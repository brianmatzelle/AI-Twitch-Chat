# will be for the chat window
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize
from chat_components import ResizeHandle, RemoveBorderButton, HeaderBar, ClearMemoryButton

class ChatWindow(QWidget):
    def __init__(self, config, bots):
        super().__init__()
        self.config = config
        self.bots = bots

        self.chat_label = QTextEdit(self)
        self.chat_label.setReadOnly(True)
        self.chat_label.setFrameStyle(0)
        self.chat_label.setStyleSheet(f"background-color: transparent; font-weight: {self.config['chat_font_weight']}; color: {self.config['chat_text_color']}; font-size: {self.config['chat_font_size']};")
        
        # Create header bar
        self.header_bar = HeaderBar(self)

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
        self.resize_handle = ResizeHandle()
        layout.addWidget(self.resize_handle, 0, Qt.AlignBottom | Qt.AlignRight)

        # Add remove border button
        self.remove_border_button = RemoveBorderButton()
        layout.addWidget(self.remove_border_button, 0, Qt.AlignBottom | Qt.AlignRight)

        # Add clear memory button
        layout.addWidget(ClearMemoryButton(self.bots), 0, Qt.AlignBottom | Qt.AlignLeft)

        self.borderFlag = True  # Flag to keep track of whether the border is visible or not
        self.setMinimumSize(300, 500)

        ### DEBUG WINDOW ###
        self.debug_window = QTextEdit(self)
        self.debug_window.setReadOnly(True)
        self.debug_window.setFrameStyle(0)
        self.debug_window.setStyleSheet("background-color: rgba(255, 255, 255, 0.8); color: black; border: 1px solid black; border-radius: 5px;")
        self.debug_window.setHidden(True)

        # Add debug toggle button to the header bar
        self.debug_toggle_button = QPushButton("Toggle Debug", self)
        self.debug_toggle_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); color: black; border: 1px solid black; border-radius: 5px; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.9); }")
        self.header_bar.layout.addWidget(self.debug_toggle_button)
        self.debug_toggle_button.clicked.connect(self.toggle_debug)

        # Update main layout
        layout.addWidget(self.debug_window)



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
        if "has left the chat!" in bot_message:
            colored_message = f'<span style="color: {bot_color};">{bot_name} {bot_message}</span><br>'
            self.chat_label.insertHtml(colored_message)
            self.chat_label.ensureCursorVisible()
            return
        elif 'has entered the chat!' in bot_message:
            colored_message = f'<span style="color: {bot_color};">{bot_name} {bot_message}</span><br>'
            self.chat_label.insertHtml(colored_message)
            self.chat_label.ensureCursorVisible()
            return
        
        else:
            colored_name = f'<span style="color: {bot_color};">{bot_name}: </span>'
            colored_message = f'<span>{bot_message}</span><br>'
            self.chat_label.insertHtml(colored_name + colored_message)  # Add the padding here
            self.chat_label.ensureCursorVisible()
            return

    def toggle_debug(self):
        if self.debug_window.isHidden():
            self.debug_window.show()
        else:
            self.debug_window.hide()

    # Add this method to update the debug window with messages
    def update_debug(self, message):
        self.debug_window.append(message)