import speech_recognition as sr
import openai
import random
import math
from bots import Bots
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QPainter
from dotenv import load_dotenv
import os

# Default configuration
config = {
    'streamer_name': 'Streamer', # Your username on Twitch or YouTube or whatever
    'num_bots': 4,              # Number of bots in your chat
    'bot_update_interval': 10,  # Time in seconds between bot updates (2 seconds)
    'font_size': '15px',
    'text_color': 'white',
    'border_color': 'gray',
    'font_weight': '500',
}

# Load environment variables
load_dotenv()
openai.api_key = os.environ['openai_api_key']


def chatgpt_query(prompt, max_tokens=50, temperature=0.8):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    generated_text = response.choices[0].text.strip()
    return generated_text

# Implement speech-to-text functionality
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Here, timeout is set to 10 seconds, which means the function will wait up to 10 seconds for speech input to begin. 
        # phrase_time_limit is also set to 10 seconds, which means the function will stop listening after 10 seconds of continuous speech input. 
        # You can adjust these values based on your requirements.
        audio = recognizer.listen(source, timeout=config["bot_update_interval"], phrase_time_limit=config["bot_update_interval"])  # Set the timeout and phrase time limit

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except Exception as e:
        print("Error recognizing speech:", e)
        return ""
        
# Generate bot responses
def generate_bot_responses(input_text, botsArr):
    # Determine the number of bots to respond
    max_responding_bots = math.ceil(len(botsArr) / 2) if len(botsArr) > 1 else 1
    num_responding_bots = math.ceil(len(botsArr) / random.randrange(1, max_responding_bots + 1))

    # Randomly select a quarter of the bots
    responding_bots = random.sample(botsArr, num_responding_bots)

    responses = []
    for bot in responding_bots:
        prompt = f"{input_text}"
        response = bot.chatgpt_query(prompt)
        responses.append((bot, response))
    return responses
        
class SpeechRecognitionThread(QThread):
    new_response = pyqtSignal(object)

    def __init__(self, bots):
        super().__init__()
        self.bots = bots

    def run(self):
        while True:
            input_text = speech_to_text()
            if input_text.lower() == 'exit':
                break

            if input_text.strip():
                bot_responses = generate_bot_responses(input_text, self.bots.arr)
                for bot, response in bot_responses:
                    self.new_response.emit((bot, response))

class HeaderBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

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
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def sizeHint(self):
        return QSize(12, 12)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.drawRect(0, 0, self.width(), self.height())


class TransparentChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.chat_label = QTextEdit(self)
        self.chat_label.setReadOnly(True)
        self.chat_label.setFrameStyle(0)
        self.chat_label.setStyleSheet(f"background-color: transparent; font-weight: {config['font_weight']}; color: {config['text_color']}; font-size: {config['font_size']};")
        # Create header bar with minimize, maximize, and exit buttons
        self.header_bar = HeaderBar(self)
        self.header_layout = QHBoxLayout()

        # Set the background color of the header bar
        self.header_bar.setStyleSheet("background-color: lightgray; text-align: center; border: none; font-size: 12px; font-weight: bold; padding: 2px;")

        self.minimize_button = QPushButton("_")
        self.maximize_button = QPushButton("[]")
        self.exit_button = QPushButton("X")

        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self.toggleMaximized)
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #ff0000;")

        self.header_layout.addWidget(self.minimize_button)
        self.header_layout.addWidget(self.maximize_button)
        self.header_layout.addWidget(self.exit_button)
        self.header_bar.setLayout(self.header_layout)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.header_bar)
        layout.addWidget(self.chat_label)
        self.setLayout(layout)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(f"padding: 5px; color: black; border: 3px solid {config['border_color']}; border-top: 5px solid {config['border_color']}; border-radius: 5px;")
        self.setWindowTitle(config['streamer_name'] + "'s Chat")
        self.setGeometry(100, 100, 400, 600)

        self.oldPos = None

        self.setMouseTracking(True)
        self.resizing = False
        self.resize_border_size = 40  # Increase this value to make the border larger

        # Add resize handle
        self.resize_handle = ResizeHandle(self)
        layout.addWidget(self.resize_handle, 0, Qt.AlignBottom | Qt.AlignRight)
        layout.setContentsMargins(0, 0, 0, 0)  # Add a bottom margin to move the handle up

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            if self.resize_handle.geometry().contains(event.pos()):
                self.resizing = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.oldPos:
            if not self.resizing:
                delta = event.globalPos() - self.oldPos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()
            else:
                new_size = QSize(event.pos().x(), event.pos().y())
                self.resize(new_size)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None
            self.resizing = False

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def update_chat(self, bot_name, bot_message, bot_color):
        colored_name = f'<span style="color: {bot_color};">{bot_name}: </span>'
        colored_message = f'<span>{bot_message}</span><br>'
        # padding = '<br>&nbsp;'  # Add this line to create padding between messages
        # self.chat_label.insertHtml(colored_name + colored_message + padding)  # Add the padding here
        self.chat_label.insertHtml(colored_name + colored_message)  # Add the padding here
        self.chat_label.ensureCursorVisible()

def user_interface():
    app = QApplication([])

    bots = Bots(config['num_bots'])

    print("Chat.tv started. Start talking or type 'exit' to quit.")
    chat_window = TransparentChatWindow()
    chat_window.show()

    speech_recognition_thread = SpeechRecognitionThread(bots)
    speech_recognition_thread.new_response.connect(lambda response: chat_window.update_chat(response[0].name, response[1], response[0].color))
    speech_recognition_thread.start()

    app.exec()

def main():
    user_interface()

if __name__ == "__main__":
    main()