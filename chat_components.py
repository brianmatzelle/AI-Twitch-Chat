from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QIcon
from header_components import LogoIcon, ChatTvLabel, MinimizeButton, MaximizeButton, ExitButton
from footer_components import ResizeHandle, RemoveBorderButton, ClearMemoryButton

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
        self.layout.addWidget(MaximizeButton(self))
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

class FooterBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: lightgray; text-align: center; border: none; font-size: 12px; font-weight: bold;")
        self.layout = QHBoxLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(ResizeHandle())
        self.layout.addWidget(RemoveBorderButton())
        self.layout.addWidget(ClearMemoryButton(self.parent.bots))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)