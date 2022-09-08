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

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtGui import QTextCursor

from main_view import Ui_MainWindow
from app_logging import getLogger

log = getLogger("view")

class AppWindow(QMainWindow, Ui_MainWindow):

    btn_click_signal = Signal()
    show_msg_on_statusbar_signal = Signal(str)
    show_txt_on_edit_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.handleClick)

        self.show_msg_on_statusbar_signal.connect(self.showMessageOnStatusBar)

        self.textEdit.setReadOnly(True)
        self.show_txt_on_edit_signal.connect(self.showTxtOnTextEdit)


        self.comboBox.addItem("hello")
        self.comboBox.addItem("hellll")
    def handleClick(self):
        log.info("click")
        self.btn_click_signal.emit()
    
    def handleComboBoxClick(self):
        log.debug("ComboBox Clicked")

    def showMessageOnStatusBar(self, message):
        self.statusbar.showMessage(message)
    

    def showTxtOnTextEdit(self, txt):
        # tc = self.textEdit.textCursor()
        # tc.movePosition(QTextCursor.End)
        # tc.insertText(txt)

        self.textEdit.moveCursor(QTextCursor.End)
        self.textEdit.insertPlainText(txt)
        self.textEdit.moveCursor(QTextCursor.End)
        


application = QApplication()
appWindow = AppWindow()
