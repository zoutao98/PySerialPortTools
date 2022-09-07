from threading import Thread
import app_logging

from app_instance import application, appWindow
from serial_port_thread import start_serial_port

log = app_logging.getLogger("app")

showStr = ["button", "ddd"]

def btn_click():
    def thread_func():
        log.info("btn_click")
        appWindow.show_statusbar.emit("thread call")
    thread1 = Thread(target=thread_func, name="SerialThread")
    
    thread1.start()

if __name__ == '__main__':
    appWindow.btn_click_singl.connect(btn_click)
    start_serial_port()
    appWindow.show()
    application.exec_()
