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
import serial
from threading import Thread
import serial_asyncio

from app_instance import appWindow
from app_logging import getLogger

from PySide2 import QtSerialPort

_log = getLogger("serial")

__port_name = None

class SerailDevice():
    def __init__(self) -> None:
        self.serial = serial.Serial()


class SerialPortProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        
    def connection_lost(self, exc):
        _log.warn('port closed')
        asyncio.get_event_loop().stop()
    def data_received(self, data):
        appWindow.show_txt_on_edit_signal.emit(data.decode('utf-8'))

def serial_thread_loop_task(loop):
    global __port_name
    coro = serial_asyncio.create_serial_connection(loop, SerialPortProtocol, __port_name, baudrate=115200)
    loop.run_until_complete(coro)
    loop.run_forever()


def serial_thread_func():
    _log.debug("thread run")

def start_serial_port():
    # my_serial_thread = Thread(target=serial_thread_loop_task, args=(asyncio.new_event_loop(),))
    # my_serial_thread.daemon = True
    # my_serial_thread.start()
    import app_instance
    if (len(app_instance.port_list) > 0) and (appWindow.comboBox.currentIndex() > 0):
        global __port_name
        __port_name = app_instance.port_list[appWindow.comboBox.currentIndex() - 1].name
        _log.debug(__port_name)
        appWindow.btn_change_signal.emit()
        # _serail_thread = Thread(name="SerialThread", target=serial_thread_func)
        # _log.debug(_serail_thread.is_alive())
        # _serail_thread.start()
    else:
        appWindow.show_msg_on_notice_signal.emit("please select serial port !")
        appWindow.show_msg_on_statusbar_signal.emit("please select serial port !", 0)

appWindow.btn_click_signal.connect(start_serial_port)