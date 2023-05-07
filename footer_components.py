from PyQt5.QtWidgets import QWidget, QSizePolicy, QPushButton
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSize, Qt

class ResizeHandle(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def sizeHint(self):
        return QSize(12, 12)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.drawRect(0, 0, self.width(), self.height())

class RemoveBorderButton(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def sizeHint(self):
        return QSize(12, 12)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.gray)
        painter.drawRect(0, 0, self.width(), self.height())

class ClearMemoryButton(QPushButton):
    def __init__(self, bots):
        super().__init__()
        self.bots = bots
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText('⟳')
        self.setStyleSheet("QPushButton {font-weight: bold; font-size: 18px; background-color: white; border: none;} QPushButton:hover {background-color: lightgray;}")
        self.setContentsMargins(0, 0, 0, 0)
        self.clicked.connect(self.bots.clear_memory)
