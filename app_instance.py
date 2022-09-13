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

import typing
from PySide2.QtCore import Signal, QObject, QThread, QTimer, Qt
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QWidget
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
            self.comboBox.clear()
            self.comboBox.addItem("please select serial port")
            global port_list 
            port_list = serial.tools.list_ports.comports()
            if len(port_list) <= 0:
                _log.error("No serial port found")
            else:
                for __port in port_list:
                    self.comboBox.addItem(__port.description)
        return super().eventFilter(watched, event)

comboBoxEventFilter = ComboBoxEventFilter()

class NoticeWidget(QLabel):
    _parent = None

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setParent(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setVisible(True)
        self.setStyleSheet("color: white;background-color:rgba(80, 80, 80, 255);border-radius:7px;")
        self.installEventFilter(self)
        self.changeSize()
        self.timer = QTimer()

        self.timer.start(1000)
        self.timer.timeout.connect(self.handleTimeOut)
    
    def changeSize(self):
        if self._parent:
            w = self._parent.width() * 0.5
            self.setFixedSize(w, 30)
            self.move((self._parent.width() - self.width()) >> 1, (self._parent.height() - self.height()) >> 1)
    
    def handleTimeOut(self):
        self.timer.stop()
        self.deleteLater()
    
    def eventFilter(self, watched, event):
        if event.type() == event.Paint:
            self.changeSize()
        return super().eventFilter(watched, event)

class AppWindow(QMainWindow, Ui_MainWindow):

    btn_click_signal = Signal()
    btn_change_signal = Signal()
    show_msg_on_statusbar_signal = Signal(str, int)
    show_txt_on_edit_signal = Signal(str)
    show_msg_on_notice_signal = Signal(str)

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
        self.show_msg_on_notice_signal.connect(self.showMsgOnNotice)
        

    def handleClick(self):
        self.btn_click_signal.emit()
    def showMsgOnNotice(self, msg):
        self.noticeWidget = NoticeWidget(self)
        self.noticeWidget.setText(msg)
    def handleBtnChange(self):
        self.pushButton.setText("关闭串口")
    
    def showMessageOnStatusBar(self, message, timeout):
        self.statusbar.showMessage(message, timeout)
    
    def showTxtOnTextEdit(self, txt):
        # tc = self.textEdit.textCursor()
        # tc.movePosition(QTextCursor.End)
        # tc.insertText(txt)
        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(txt)
        self.textEdit.moveCursor(QTextCursor.End)

application = QApplication()
appWindow = AppWindow()
