import sys
from PyQt6.QtWidgets import *
from src.gui.app import MyWindow

app = QApplication(sys.argv)

window = MyWindow()
window.show()

app.exec()