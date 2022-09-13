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

from PySide2.QtCore import Signal, QObject, QThread
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtGui import QTextCursor

from main_view import Ui_MainWindow
from app_logging import getLogger

import serial.tools.list_ports

_log = getLogger("view")

port_list = serial.tools.list_ports.comports()

class ComboBoxEventFilter(QObject):
    def __init__(self) -> None:
        super().__init__()

    def setJudgeComboBox(self, comboBox):
        self.comboBox = comboBox

    def eventFilter(self, watched, event):
        if watched == self.comboBox and event.type() == event.MouseButtonPress or event.type() == event.MouseButtonDblClick:
            _log.debug(f"comboBox event: {event.type()}")
            self.comboBox.clear()
            self.comboBox.addItem("please select serial port")
            global port_list 
            port_list = serial.tools.list_ports.comports()
            _log.debug(port_list)
            if len(port_list) <= 0:
                _log.error("No serial port found")
            else:
                for __port in port_list:
                    _log.debug(__port.description)
                    _log.debug(__port.name)
                    self.comboBox.addItem(__port.description)
        return super().eventFilter(watched, event)

comboBoxEventFilter = ComboBoxEventFilter()

class AppWindow(QMainWindow, Ui_MainWindow):

    btn_click_signal = Signal()
    btn_change_signal = Signal()
    show_msg_on_statusbar_signal = Signal(str)
    show_txt_on_edit_signal = Signal(str)

    def __init__(self):
        super(AppWindow, self).__init__()
        self.setupUi(self)
        comboBoxEventFilter.setJudgeComboBox(self.comboBox)
        self.comboBox.installEventFilter(comboBoxEventFilter)

        self.pushButton.clicked.connect(self.handleClick)
        self.btn_change_signal.connect(self.handleBtnChange)

        self.show_msg_on_statusbar_signal.connect(self.showMessageOnStatusBar)

        self.textEdit.setReadOnly(True)
        self.show_txt_on_edit_signal.connect(self.showTxtOnTextEdit)

        self.comboBox.addItem("please select serial port")

    def handleClick(self):
        self.btn_click_signal.emit()
    def handleBtnChange(self):
        self.pushButton.setText("关闭串口")
    
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
