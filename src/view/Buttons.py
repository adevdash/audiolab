from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton

class PlayPause(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Play")
        self.setCheckable(True)
        self.clicked.connect(self.onClick)
        self.setMinimumSize(QSize(100, 50))

    def onClick(self):
        if self.isChecked():
            self.setText("Pause")
            # Add code to start playing audio
        else:
            self.setText("Play")
            # Add code to pause audio