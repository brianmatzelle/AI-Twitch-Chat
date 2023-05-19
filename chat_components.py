from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPainter, QIcon
from header_components import LogoIcon, ChatTvLabel, MinimizeButton, MaximizeButton, ExitButton
from footer_components import RemoveBorderButton, BotCountWidget

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

def ClearMemoryButton(parent):
    clear_memory_button = QPushButton('⟳')
    clear_memory_button.clicked.connect(lambda: parent.bots.clear_memory(parent))
    clear_memory_button.clicked.connect(lambda: parent.clear_chat())
    clear_memory_button.setStyleSheet("QPushButton {font-weight: bold; font-size: 12px; background-color: rgba(255, 255, 255, 0.8); border: none;} QPushButton:hover {background-color: lightgray;}")
    clear_memory_button.setContentsMargins(0, 0, 0, 0)
    return clear_memory_button

class FooterBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: lightgray; text-align: center; border: none; font-size: 12px; font-weight: bold;")

        self.layout = QHBoxLayout()
        self.left_layout = QHBoxLayout()

        # bot count label
        self.bot_count_label = BotCountWidget(0)
        self.left_layout.addWidget(self.bot_count_label)

        # listening label
        self.listening_label = QLabel("👂🏼", self)
        self.listening_label.setStyleSheet("color: white; font-size: 16px; background-color: transparent; border: none;")
        self.listening_label.setHidden(True)
        self.left_layout.addWidget(self.listening_label)

        # recognizing label
        self.recognizing_label = QLabel("🤔", self)
        self.recognizing_label.setStyleSheet("color: white; font-size: 16px; background-color: transparent; border: none;")
        self.recognizing_label.setHidden(True)
        self.left_layout.addWidget(self.recognizing_label)

        # Responding loading label
        self.responding_label = QLabel("🤖💭", self)
        self.responding_label.setStyleSheet("color: white; font-size: 16px; background-color: transparent; border: none;")
        self.responding_label.setHidden(True)
        self.left_layout.addWidget(self.responding_label)

        # set left layout
        self.layout.addLayout(self.left_layout)
        self.layout.addStretch(1)

        # Remove Border Button
        self.remove_border_button = RemoveBorderButton(parent)
        self.layout.addWidget(self.remove_border_button)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


    def show_listening(self, isListening):
        if isListening:
            self.listening_label.setHidden(False)
        else:
            self.listening_label.setHidden(True)

    def show_recognizing(self, isRecognizing):
        if isRecognizing:
            self.recognizing_label.setHidden(False)
        else:
            self.recognizing_label.setHidden(True)

    def show_responding(self, isResponding):
        if isResponding:
            self.responding_label.setHidden(False)
        else:
            self.responding_label.setHidden(True)

    def toggleBorderText(self):
        self.remove_border_button.setText('show' if self.parent.borderFlag else 'hide')

    def updateBotCount(self):
        botsCount = len(self.parent.bots.arr)
        self.bot_count_label.setText(f"🧍🏼 {botsCount}")