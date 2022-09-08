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

from PySide2.QtCore import Signal, QObject
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtGui import QTextCursor

from main_view import Ui_MainWindow
from app_logging import getLogger

import serial.tools.list_ports

log = getLogger("view")

class AppWindow(QMainWindow, Ui_MainWindow):

    btn_click_signal = Signal()
    show_msg_on_statusbar_signal = Signal(str)
    show_txt_on_edit_signal = Signal(str)

    def __init__(self):
        super(AppWindow, self).__init__()
        self.setupUi(self)
        self.comboBox.installEventFilter(self)

        self.pushButton.clicked.connect(self.handleClick)

        self.show_msg_on_statusbar_signal.connect(self.showMessageOnStatusBar)

        self.textEdit.setReadOnly(True)
        self.show_txt_on_edit_signal.connect(self.showTxtOnTextEdit)


        self.comboBox.addItem("serial port")
    
    def eventFilter(self, watched, event):
        if watched == self.comboBox and event.type() == event.MouseButtonPress or event.type() == event.MouseButtonDblClick:
            log.info(f"comboBox event {event.type()}")
            self.comboBox.clear()
            __port_list = serial.tools.list_ports.comports()
            if len(__port_list) <= 0:
                log.error("No serial port found")
            else:
                for __port in __port_list:
                    log.info(__port.description)
                    log.info(__port.name)
                    self.comboBox.addItem(__port.description)
        return super(AppWindow, self).eventFilter(watched, event)
        # return False
    
    def handleClick(self):
        log.info("click")
        self.btn_click_signal.emit()
    
    def handleComboBoxClick(self):
        log.debug("ComboBox Clicked")

    def showMessageOnStatusBar(self, message):
        self.statusbar.showMessage(message, 500)
    

    def showTxtOnTextEdit(self, txt):
        # tc = self.textEdit.textCursor()
        # tc.movePosition(QTextCursor.End)
        # tc.insertText(txt)
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(txt)
        self.textEdit.moveCursor(QTextCursor.End)
    

    
        


application = QApplication()
appWindow = AppWindow()
