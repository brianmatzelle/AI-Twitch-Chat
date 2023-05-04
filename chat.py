# will be for the chat window
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize
from chat_components import ResizeHandle, RemoveBorderButton, HeaderBar

class ChatWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.chat_label = QTextEdit(self)
        self.chat_label.setReadOnly(True)
        self.chat_label.setFrameStyle(0)
        self.chat_label.setStyleSheet(f"background-color: transparent; font-weight: {self.config['chat_font_weight']}; color: {self.config['chat_text_color']}; font-size: {self.config['chat_font_size']};")
        
        ### HEADER BAR --------------------------------------------------------------- ###

        # Create header bar with "Chat.tv" label, minimize, maximize, and exit buttons
        self.header_bar = HeaderBar(self)
        self.header_layout = QHBoxLayout()

        # Set the background color of the header bar
        self.header_bar.setStyleSheet("background-color: lightgray; text-align: center; border: none; font-size: 12px; font-weight: bold;")

        # Create QLabel for the icon with hyperlink
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)  # You can adjust the size of the icon
        self.icon_label.setOpenExternalLinks(True)
        self.icon_label.setStyleSheet("border: none; padding: 0px; margin: 0px;")
        self.icon_label.setText('<a href="https://brianmatzelle.com"><img src="assets/blanc32x32.png" /></a>')
        self.icon_label.setContentsMargins(0, 0, 0, 0)
        
        # Create QLabel for the "Chat.tv" label with hyperlink
        self.chat_tv_label = QLabel()
        self.chat_tv_label.setOpenExternalLinks(True)
        self.chat_tv_label.setText(f"CHAT.TV: {self.config['streamer_name']}'s chat")
        self.chat_tv_label.setStyleSheet("background-color: #243049; padding-left: 5px; color: lightgray; font-size: 12px; font-weight: bold; border: none; border-radius: 0px; margin: 0px;")
        self.chat_tv_label.setContentsMargins(0, 0, 0, 0)

        # Create a QHBoxLayout for the left side of the header
        left_layout = QHBoxLayout()
        left_layout.addWidget(self.icon_label)
        left_layout.addWidget(self.chat_tv_label)
        
        # Create the minimize, maximize, and exit buttons
        self.minimize_button = QPushButton("_")
        self.maximize_button = QPushButton("[]")
        self.exit_button = QPushButton("X")

        # Style the header buttons
        self.minimize_button.setStyleSheet("QPushButton {width: 30px; background-color: lightgray;} QPushButton:hover {background-color: gray;}")
        self.maximize_button.setStyleSheet("QPushButton {width: 30px; background-color: lightgray;} QPushButton:hover {background-color: gray;}")
        self.exit_button.setStyleSheet("QPushButton {width: 30px; background-color: #243049; color: lightgray;} QPushButton:hover {background-color: #e60000;}")

        # Add functionality to the header buttons
        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggleMaximized)
        self.exit_button.clicked.connect(self.close)

        # Add left_layout to header_layout
        self.header_layout.addLayout(left_layout)
        self.header_layout.addStretch(1)  # Add stretch factor to push the buttons to the right
        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.maximize_button)
        self.header_layout.addWidget(self.exit_button)
        self.header_bar.setLayout(self.header_layout)

        ### END HEADER BAR ------------------------------------------------------------ ###

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.header_bar)
        layout.addWidget(self.chat_label)
        self.setLayout(layout)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(f"padding: 5px; color: black; border: 3px solid {self.config['chat_border_color']}; border-top: 5px solid {self.config['chat_border_color']}; border-radius: 5px;")
        self.setWindowTitle(self.config['streamer_name'] + "'s Chat")
        self.setGeometry(100, 100, 400, 600)

        self.oldPos = None

        self.setMouseTracking(True)
        self.resizingFlag = False
        self.resize_border_size = 40  # Increase this value to make the border larger

        # Add resize handle
        self.resize_handle = ResizeHandle(self)
        layout.addWidget(self.resize_handle, 0, Qt.AlignBottom | Qt.AlignRight)

        # Add remove border button
        self.remove_border_button = RemoveBorderButton(self)
        layout.addWidget(self.remove_border_button, 0, Qt.AlignBottom | Qt.AlignRight)

        self.borderFlag = True  # Flag to keep track of whether the border is visible or not
        self.setMinimumSize(300, 500)



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            if self.resize_handle.geometry().contains(event.pos()):
                self.resizingFlag = True
            if self.remove_border_button.geometry().contains(event.pos()):
                if self.borderFlag:
                    self.setStyleSheet("padding: 5px; background-color: transparent; border: none; border-radius: 5px")
                    self.header_bar.hide()
                else:
                    self.setStyleSheet(f"padding: 5px; color: black; border: 3px solid {self.config['chat_border_color']}; border-top: 5px solid {self.config['chat_border_color']}; border-radius: 5px;")
                    self.header_bar.show()
                self.borderFlag = not self.borderFlag
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.oldPos:
            if not self.resizingFlag:
                delta = event.globalPos() - self.oldPos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()
            else:
                new_size = QSize(event.pos().x(), event.pos().y())
                self.resize(new_size)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None
            self.resizingFlag = False

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def update_chat(self, bot_name, bot_message, bot_color):
        colored_name = f'<span style="color: {bot_color};">{bot_name}: </span>'
        colored_message = f'<span>{bot_message}</span><br>'
        self.chat_label.insertHtml(colored_name + colored_message)  # Add the padding here
        self.chat_label.ensureCursorVisible()