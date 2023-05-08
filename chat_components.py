from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QIcon
from header_components import LogoIcon, ChatTvLabel, MinimizeButton, MaximizeButton, ExitButton

class HeaderBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: lightgray; text-align: center; border: none; font-size: 12px; font-weight: bold;")
        
        # logo, "Chat.tv" label, minimize, maximize, and exit buttons
        self.layout = QHBoxLayout()
        self.left_layout = QHBoxLayout()
        self.left_layout.addWidget(LogoIcon())
        self.left_layout.addWidget(ChatTvLabel(self.parent.config))
        self.layout.addLayout(self.left_layout)
        self.layout.addStretch(1)
        self.layout.addWidget(MinimizeButton(self))
        self.layout.addWidget(ExitButton(self))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.parent.oldPos:
            delta = event.globalPos() - self.parent.oldPos
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.parent.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.oldPos = None

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

def ClearMemoryButton(parent):
    clear_memory_button = QPushButton('⟳')
    clear_memory_button.clicked.connect(lambda: parent.bots.clear_memory(parent))
    clear_memory_button.setStyleSheet("QPushButton {font-weight: bold; font-size: 12px; background-color: white; border: none;} QPushButton:hover {background-color: lightgray;}")
    clear_memory_button.setContentsMargins(0, 0, 0, 0)
    return clear_memory_button
