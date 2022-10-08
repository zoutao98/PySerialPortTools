from PySide2.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction
from PySide2.QtGui import QIcon

app = QApplication()

main_window = QMainWindow()

system_tray_icon = QSystemTrayIcon()
system_tray_icon.setIcon(QIcon("icon.png"))
system_tray_icon.setVisible(True)

menu = QMenu()
entries = ["One", "Two", "Three"]
for entry in entries:
    action = QAction(entry)
    menu.addAction(action)
    action.triggered.connect(app.quit)

system_tray_icon.setContextMenu(menu)

main_window.show()

app.exec_()