import asyncio
from asyncio.log import logger
import logging
import statistics
from time import sleep, time
import traceback, sys
from serial_asyncio import open_serial_connection
from .utlis import *

RETRY_TIMER = 5


class PemsRequest:
    ''' Basic class used to encapsulate a client request

    inputs:
        transport (asyncio.BaseTransport): Transport used to for the reply message
        data (bytes): data to send on the serial port
    '''

    def __init__(self, transport: asyncio.BaseTransport, data: bytes) -> None:
        self.transport = transport
        self.data = data


async def run_guarded(aw):
    try:
        await aw
    except:
        traceback.print_exc()
        sys.exit(1)
        
        
class Handler():
    ''' Main orchestrator that handles the request on the serial port

    inputs:
        loop (asyncio.AbstractEventLoop): event loop on which the handler will run
        serial_settings (dict): dict containing kwargs with the serial configuration
                                {'url': _,'baudrate': _, 'parity': _, 'stopbits': _, 'bytesize': _}
        serial_timeout (int): time after which a message is considered timedout
        port_tcp (int): TCP port on which the server will listen
        retry_connection (bool): if True, will try to reopen the server and the serial port on failure
    '''

    def __init__(self, serial_settings: dict, serial_timeout: int, port_tcp: int, retry_connection: bool = False) -> None:
        self.serial_settings = serial_settings
        self.port_tcp = port_tcp
        self.serial_timeout = serial_timeout
        self.retry_connection = retry_connection
        self.request_queue = []
        self.request_in_progress = False
        self.last_request = None
        self.last_slave_request = None
        self.reader = None
        self.writer = None
        self.buffer = b''
        self.time_passed_serial_message = 0
        self.timeout_task = None
        self.start_time_message = None
        self.slaves_timeout_counter = {}
        self.blacklisted_slaves_timer = {}
        self.message_timers = {}
        
    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        ''' Starts the server
        '''
        self.loop = loop
        while True:
            try:
                server_coro = self.loop.create_server(lambda: TCPServerProtocol(self),
                                                      '0.0.0.0',
                                                      self.port_tcp)
                self.server = self.loop.run_until_complete(server_coro)
                logging.info('listening on {}:{}'.format('0.0.0.0', self.port_tcp))
                break
            except Exception as e:
                logging.exception(e)
                if self.retry_connection:
                    logging.warning('retrying to open the server in {} seconds'.format(RETRY_TIMER))
                    sleep(RETRY_TIMER)
                else:
                    sys.exit(1)

        self.serial_task = self.loop.create_task(run_guarded(self.run_serial()))
        self.unblacklister_task = self.loop.create_task(run_guarded(self.unblacklist_slaves()))
        self.print_info_task = self.loop.create_task(run_guarded(self.print_info()))
        
    def stop(self) -> None:
        ''' Stops the server and the serial port
        '''
        if self.server:
            self.server.close()
            self.server = None
        if self.writer:
            self.writer.close()
            self.writer = None
        if self.serial_task:
            self.serial_task.cancel()
            self.serial_task = None
        if self.unblacklister_task:
            self.unblacklister_task.cancel()
            self.unblacklister_task = None
        if self.print_info_task:
            self.print_info_task.cancel()
            self.print_info_task = None
        self.loop.stop()
        
    def __del__(self) -> None:
        ''' Ensures the server and the serial port are closed on deletion
        '''
        self.stop()
        self

    def send_new_request_from_queue(self) -> None:
        ''' Sends the next available request from the queue
        '''
        if self.request_in_progress:
            return
        self.last_request = None

        if self.request_queue:
            self.last_request = self.request_queue.pop(0)
            slave = get_pems_slave(self.last_request.data)

            # if the request queue is not empty, check if the request must be discarded
            if self.blacklisted_slaves_timer.get(slave, 0) > 0 and self.request_queue:
                for r in self.request_queue:
                    if self.blacklisted_slaves_timer.get(get_pems_slave(r.data), 0) == 0:
                        logging.debug('ignored request for slave {} because it\'s blacklisted for additional {} seconds'.format(slave, self.blacklisted_slaves_timer[slave]))
                        try:
                            self.last_request.transport.write(create_ignored_message(slave))
                        except Exception as e:
                            logging.exception(e)
                        self.send_new_request_from_queue()
                        return

            self.request_in_progress = True
            self.last_slave_request = slave
            self.write_message_to_serial(self.last_request)

    def write_message_to_serial(self, p_rquest: PemsRequest) -> None:
        ''' Writes the request to the serial port

        inputs:
            p_rquest (PemsRequest): object containing information to send on the serial
        '''
        if self.writer:
            try:
                logging.debug('sending message to serial {}'.format(p_rquest.data))
                self.buffer = b''
                self.time_passed_serial_message = 0
                self.writer.write(p_rquest.data)
                self.start_timeout_timer()
            except Exception as e:
                logging.exception(e)
                sys.exit(1)
        else:
            logging.debug('serial not initialized, ignoring message')
            try:
                p_rquest.transport.write(create_ignored_message(get_pems_slave(p_rquest.data)))
            except Exception:
                logging.exception()
            finally:
                self.request_in_progress = False
                self.last_request = None

    async def run_serial(self) -> None:
        ''' Used in a coroutine to open the serial port and read the data
        '''
        while not self.writer:
            try:
                self.reader, self.writer = await open_serial_connection(**self.serial_settings)
                logging.info('successfully opened serial device {}'.format(self.serial_settings['url']))
            except Exception as e:
                if self.retry_connection:
                    self.reader = None
                    self.writer = None
                    logging.warning('failed to open port {}, retrying in {} seconds'.format(self.serial_settings['url'], RETRY_TIMER))
                    logging.exception(e)
                    await asyncio.sleep(RETRY_TIMER)
                else:
                    logging.error('failed to open port {}'.format(self.serial_settings['url']))
                    sys.exit(1)

        while True:
            try:
                data = await self.reader.read(100000)
            except Exception as e:
                logging.exception(e)
                sys.exit(1)
            self.buffer += data

            slave_index = 0

            try:
                # discard the bytes until we it's equal to the number of the slave we sent last message
                while slave_index < len(self.buffer) and self.buffer[slave_index] != self.last_slave_request:
                    slave_index += 1
                if slave_index > 0:
                    self.buffer = self.buffer[slave_index:]
            except Exception as e:
                self.buffer = b''
                logging.error(e)

            if is_message_complete(self.buffer):
                logging.debug('new message from serial {}'.format(self.buffer))
                self.time_passed_serial_message += self.stop_timeout_timer()
                self.request_in_progress = False
                slave = get_pems_slave(self.buffer)
                if slave in self.message_timers:
                    self.message_timers[slave].append(self.time_passed_serial_message)
                else:
                    self.message_timers[slave] = [self.time_passed_serial_message]
                self.time_passed_serial_message = 0

                self.slaves_timeout_counter[slave] = 0
                if self.blacklisted_slaves_timer.get(slave, 0) > 0:
                    logging.debug('removed slave {} from blacklist beacuse of a new message'.format(slave))
                self.blacklisted_slaves_timer[slave] = 0
                try:
                    self.last_request.transport.write(self.buffer)
                except Exception as e:
                    logging.exception(e)
                finally:
                    self.buffer = b''
                    self.send_new_request_from_queue()
            else:
                if self.request_in_progress and self.time_passed_serial_message*1000 < self.serial_timeout:
                    self.time_passed_serial_message += self.stop_timeout_timer()
                    self.start_timeout_timer()
                await asyncio.sleep(0.006)

    async def unblacklist_slaves(self) -> None:
        ''' Used in a coroutine. Decreases the timer of blacklisted slaves until 0
        '''
        while True:
            for slave, timer in self.blacklisted_slaves_timer.items():
                self.blacklisted_slaves_timer[slave] = max(timer-0.1, 0)
            await asyncio.sleep(0.1)

    async def print_info(self) -> None:
        ''' Prints periodic information
        '''
        while True:
            await asyncio.sleep(60)
            logger.info("Slaves information: \n{}".format('\n'.join("slave {} average response time: {}ms, min: {}ms, max: {}ms".format(slave,
                                                                                                                                        int(statistics.mean(timer)*1000),
                                                                                                                                        int(min(timer)*1000),
                                                                                                                                        int(max(timer)*1000))
                                                                    for slave, timer in self.message_timers.items())))

            for timer in self.message_timers.values():
                timer.clear()

    def start_timeout_timer(self) -> None:
        ''' Starts timeout timer for the serial message
        '''
        if self.timeout_task:
            self.stop_timeout_timer()
        self.start_time_message = time()
        self.timeout_task = asyncio.ensure_future(self.timeout())

    def stop_timeout_timer(self) -> float:
        ''' Stops timeout timer for the serial message
        '''
        if not self.timeout_task:
            return 0
        
        self.timeout_task.cancel()
        self.timeout_task = None
        return time() - self.start_time_message

    async def timeout(self) -> None:
        ''' Handles message timeout
        '''
        await asyncio.sleep(self.serial_timeout/1000)

        self.timeout_task = None
        self.request_in_progress = False
        if not self.last_request:
            self.send_new_request_from_queue()
            return

        slave = get_pems_slave(self.last_request.data)
        logging.debug('message timeout for slave {}'.format(slave))

        new_timeout_counter = min(self.slaves_timeout_counter.get(slave, 0) + 1, pems_consts.PEMS_MASTER_BLACKLIST_TIMEOUTS)
        self.slaves_timeout_counter[slave] = new_timeout_counter

        if new_timeout_counter >= pems_consts.PEMS_MASTER_BLACKLIST_TIMEOUTS:
            new_timeout_timer = min(pems_consts.PEMS_SCHEDULER_BLACKLIST_TIME_BASE*len(self.slaves_timeout_counter), pems_consts.PEMS_SCHEDULER_BLACKLIST_TIME_MAX)
            self.blacklisted_slaves_timer[slave] = new_timeout_timer
            logging.debug('slave {} blacklisted for {} seconds because of {} or more consecutive timeouts'.format(slave, new_timeout_timer, new_timeout_counter))
        elif new_timeout_counter >= pems_consts.PEMS_MASTER_CONGESTION_TIMEOUTS:
            new_timeout_timer = min(pems_consts.PEMS_SCHEDULER_CONGESTION_TIME_BASE*len(self.slaves_timeout_counter), pems_consts.PEMS_SCHEDULER_CONGESTION_TIME_MAX)
            self.blacklisted_slaves_timer[slave] = new_timeout_timer
            logging.debug('slave {} throttled for {} seconds because of {} or more consecutive timeouts'.format(slave, new_timeout_timer, new_timeout_counter))

        try:
            self.last_request.transport.write(create_timeout_message(slave))
        except Exception as e:
            logging.exception(e)
        self.last_request = None
        self.send_new_request_from_queue()


class TCPServerProtocol(asyncio.Protocol):
    ''' Created on new connection from client

    inputs: handler (Handler)
    '''

    def __init__(self, handler: Handler) -> None:
        self.handler = handler
        asyncio.Protocol.__init__(self)

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        peername = transport.get_extra_info('peername')
        logging.debug('connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        logging.debug('new request received: {}'.format(data))

        if get_pems_type(data) == pems_types.CMD_READ_ACCESS_ID:
            self.handle_access_id(get_pems_slave(data))
            return

        if self.handler.writer is None:
            self.transport.write(create_port_unavailable_message(get_pems_slave(data)))
            return

        if self.handler.last_request and self.handler.last_request.transport == self.transport:
            # client already asking another request, ignore it
            return

        # delete previous request if present
        for index, p_request in enumerate(self.handler.request_queue):
            if p_request.transport == self.transport:
                self.handler.request_queue.remove(index)
                break

        self.handler.request_queue.append(PemsRequest(transport=self.transport, data=data))
        self.handler.send_new_request_from_queue()

    def connection_lost(self, exc: Exception) -> None:
        logging.debug('connection lost with client: {}{}'.format(self.transport.get_extra_info('peername'),
                                                                 ', error: {}'.format(exc) if exc else ''))

    def handle_access_id(self, slave: int) -> None:
        ''' Used to reply to onboard special message
        '''
        try:
            self.transport.write(create_access_id_message(slave))
        except Exception as e:
            logging.exception(e)
