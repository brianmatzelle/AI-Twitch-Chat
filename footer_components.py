from PyQt5.QtWidgets import QWidget, QSizePolicy, QPushButton
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QSize, Qt

class RemoveBorderButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText('hide border')
        self.setStyleSheet("QPushButton {color: rgb(54, 69, 79); font-weight: bold; font-size: 12px; background-color: rgba(26, 26, 26, 0.4); border: none;} QPushButton:hover {background-color: rgba(26, 26, 26, 0.9);}")
        self.setContentsMargins(0, 0, 0, 0)
        self.clicked.connect(self.parent.toggleBorder)

class ClearMemoryButton(QPushButton):
    def __init__(self, bots):
        super().__init__()
        self.bots = bots
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setText('⟳')
        self.setStyleSheet("QPushButton {font-weight: bold; font-size: 18px; background-color: white; border: none;} QPushButton:hover {background-color: lightgray;}")
        self.setContentsMargins(0, 0, 0, 0)
        self.clicked.connect(self.bots.clear_memory)
