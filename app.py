from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PySide2.QtCore import QUrl
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

import app_logging
from main_view import Ui_MainWindow

log = app_logging.getLogger("app")

showStr = ["button", "ddd"]

def handleClick():
    log.info("click")

class AppWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication()

    appWindow = AppWindow()
    appWindow.show()
    # qtWebBrowser = QWebEngineView()
    # qtWebBrowser.load(QUrl("http://www.baidu.com"))
    # qtWebBrowser.show()
    app.exec_()
