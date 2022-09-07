import asyncio
from threading import Thread
import serial_asyncio

from app_logging import getLogger

log = getLogger("serial")


class SerialPortProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        
    def connection_lost(self, exc):
        log.warn('port closed')
        asyncio.get_event_loop().stop()
    def data_received(self, data):
        log.info(data)




def serial_thread_loop_task(loop):
    coro, protocol = serial_asyncio.create_serial_connection(loop, SerialPortProtocol, "COM58", baudrate=115200)
    loop.run_until_complete(coro)
    loop.run_forever()

def start_serial_port():
    my_serial_thread = Thread(target=serial_thread_loop_task, args=(asyncio.new_event_loop(),))
    my_serial_thread.daemon = True
    my_serial_thread.start()