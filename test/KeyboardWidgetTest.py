from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QColor, QPalette
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, \
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QMenu, QHBoxLayout, QComboBox
import sys

sys.path.append('../src')
from view.Buttons import Keyboard, WhiteKey, BlackKey, Key

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.keyboard = Keyboard()
        self.setCentralWidget(self.keyboard)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()