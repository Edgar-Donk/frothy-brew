from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def update():
    label.setText("Updated")

def retrieve():
    print(label.text())

app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(400,400,500,300)
win.setWindowTitle("CodersLegacy")

label = QtWidgets.QLabel(win)
label.setText("GUI application with PyQt5")
label.adjustSize()
label.move(100,100)

button = QtWidgets.QPushButton(win)
button.clicked.connect(update)
button.setText("Update Button")
button.move(100,150)

button.setStyleSheet("background-color: red;font-size:18px;font-family:Times New Roman;");

button2 = QtWidgets.QPushButton(win)
button2.clicked.connect(retrieve)
button2.setText("Retrieve Button")
button2.move(100,200)

win.show()
sys.exit(app.exec_())