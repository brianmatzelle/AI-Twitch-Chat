from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize
from chat_components import  HeaderBar, ClearMemoryButton, FooterBar
from PyQt5.QtGui import QCursor

class ChatWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.bots = None

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
        self.setStyleSheet(f"padding: 5px; color: black; border: 4px solid {self.config['chat_border_color']}; border-radius: 5px;")
        self.setWindowTitle(self.config['streamer_name'] + "'s Chat")
        self.setGeometry(100, 100, 400, 600)

        self.oldPos = None

        self.setMouseTracking(True)
        self.resizingFlag = False
        self.resize_border_size = 1000  # Pixels of border that trigger resizing
        self.setCursor(Qt.ArrowCursor)

        self.borderFlag = True  # Flag to keep track of whether the border is visible or not
        self.setMinimumSize(300, 500)

        # Add clear memory button
        self.header_bar.left_layout.addWidget(ClearMemoryButton(self))

        # Toggle Background button
        self.toggle_background_button = QPushButton("◾️", self)
        self.toggle_background_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); color: black; border: 1px solid black; border-radius: 5px; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.9); }")
        self.header_bar.left_layout.addWidget(self.toggle_background_button)
        self.toggle_background_button.clicked.connect(self.toggle_chat_background)

        # Add footer bar
        self.footer_bar = FooterBar(self)
        layout.addWidget(self.footer_bar) 

        ### DEBUG WINDOW ###
        self.debug_window = QTextEdit(self)
        self.debug_window.setReadOnly(True)
        self.debug_window.setFrameStyle(0)
        self.debug_window.setStyleSheet("background-color: rgba(255, 255, 255, 0.8); color: black; border: 1px solid black; border-radius: 5px;")
        self.debug_window.setHidden(False)

        # Add debug toggle button to the header bar
        self.debug_toggle_button = QPushButton("🐞", self)
        self.debug_toggle_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); color: black; border: 1px solid black; border-radius: 5px; } QPushButton:hover { background-color: rgba(255, 255, 255, 0.9); }")
        self.header_bar.left_layout.addWidget(self.debug_toggle_button)
        self.debug_toggle_button.clicked.connect(self.toggle_debug)
        # Automatically scroll to the bottom of the debug window when new text is added
        self.debug_window.textChanged.connect(lambda: self.debug_window.verticalScrollBar().setValue(self.debug_window.verticalScrollBar().maximum()))

        # Update main layout
        layout.addWidget(self.debug_window)
        
    def assign_bots(self, bots):
        self.bots = bots

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            # Check if mouse is near the border
            if (
                abs(event.y() - self.geometry().y()) <= self.resize_border_size or
                abs(event.y() - (self.geometry().y() + self.geometry().height())) <= self.resize_border_size or
                abs(event.x() - self.geometry().x()) <= self.resize_border_size or
                abs(event.x() - (self.geometry().x() + self.geometry().width())) <= self.resize_border_size
            ):
                self.resizingFlag = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.oldPos:
            if not self.resizingFlag:
                delta = event.globalPos() - self.oldPos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()
            else:
                diff = event.globalPos() - self.oldPos
                new_width = self.width() + diff.x()
                new_height = self.height() + diff.y()
                self.resize(QSize(new_width, new_height))
                self.oldPos = event.globalPos()
            
            # Check if the mouse is near the border and set the cursor accordingly
            if (
                abs(event.y() - self.geometry().y()) <= self.resize_border_size or
                abs(event.y() - (self.geometry().y() + self.geometry().height())) <= self.resize_border_size
            ):
                self.setCursor(Qt.SizeVerCursor)  # Vertical resize cursor
            elif (
                abs(event.x() - self.geometry().x()) <= self.resize_border_size or
                abs(event.x() - (self.geometry().x() + self.geometry().width())) <= self.resize_border_size
            ):
                self.setCursor(Qt.SizeHorCursor)  # Horizontal resize cursor
        else:
            # Check if the mouse is near the border and set the cursor accordingly
            if (
                abs(event.y() - self.geometry().y()) <= self.resize_border_size or
                abs(event.y() - (self.geometry().y() + self.geometry().height())) <= self.resize_border_size
            ):
                self.setCursor(Qt.SizeVerCursor)  # Vertical resize cursor
            elif (
                abs(event.x() - self.geometry().x()) <= self.resize_border_size or
                abs(event.x() - (self.geometry().x() + self.geometry().width())) <= self.resize_border_size
            ):
                self.setCursor(Qt.SizeHorCursor)  # Horizontal resize cursor
            else:
                self.setCursor(Qt.ArrowCursor)  # Default cursor

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)  # Default cursor when the mouse leaves the widget

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None
            self.resizingFlag = False

    def toggleBorder(self):
        self.footer_bar.toggleBorderText()
        if self.borderFlag:
            self.setStyleSheet("padding: 5px; background-color: transparent; border: none; border-radius: 5px")
            self.header_bar.hide()
        else:
            self.setStyleSheet(f"padding: 5px; color: black; border: 3px solid {self.config['chat_border_color']}; border-radius: 5px;")
            self.header_bar.show()
        self.borderFlag = not self.borderFlag

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

    def update_debug(self, message):
        self.debug_window.append(message)

    def clear_debug(self):
        self.debug_window.clear()

    def clear_chat(self):
        self.chat_label.clear()

    def toggle_chat_background(self):
        if self.chat_label.styleSheet() == f"background-color: transparent; font-weight: {self.config['chat_font_weight']}; color: {self.config['chat_text_color']}; font-size: {self.config['chat_font_size']};":
            self.chat_label.setStyleSheet(f"background-color: rgba(26, 26, 26, 0.9); font-weight: {self.config['chat_font_weight']}; color: {self.config['chat_text_color']}; font-size: {self.config['chat_font_size']};")
        else:
            self.chat_label.setStyleSheet(f"background-color: transparent; font-weight: {self.config['chat_font_weight']}; color: {self.config['chat_text_color']}; font-size: {self.config['chat_font_size']};")

    