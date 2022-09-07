
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMainWindow, QApplication
from main_view import Ui_MainWindow
from app_logging import getLogger

log = getLogger("view")

class AppWindow(QMainWindow, Ui_MainWindow):

    btn_click_singl = Signal()
    show_statusbar = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.handleClick)

        self.show_statusbar.connect(self.showStatusBar)

    def handleClick(self):
        log.info("click")
        self.btn_click_singl.emit()

    def showStatusBar(self, message):
        self.statusbar.showMessage(message)


application = QApplication()
appWindow = AppWindow()
