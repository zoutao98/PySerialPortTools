#    Copyright 2022 邹涛

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import asyncio
from threading import Thread

import serial_asyncio

from app_instance import appWindow
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
        appWindow.show_txt_on_edit_signal.emit(data.decode('utf-8'))




def serial_thread_loop_task(loop):
    coro = serial_asyncio.create_serial_connection(loop, SerialPortProtocol, "COM5", baudrate=115200)
    loop.run_until_complete(coro)
    loop.run_forever()

def start_serial_port():
    my_serial_thread = Thread(target=serial_thread_loop_task, args=(asyncio.new_event_loop(),))
    my_serial_thread.daemon = True
    my_serial_thread.start()
