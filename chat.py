import speech_recognition as sr
import openai
import random
import math
from bots import Bots
from termcolor import colored
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from dotenv import load_dotenv
import os

# Default configuration
config = {
    'num_bots': 5,
    'bot_update_interval': 2,  # Time in seconds between bot updates (2 seconds)
    # Add other settings here as needed
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
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Set the timeout and phrase time limit

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
    num_responding_bots = math.ceil(len(botsArr) / 4)

    # Randomly select a quarter of the bots
    responding_bots = random.sample(botsArr, num_responding_bots)

    # Add a context for casual Twitch chat
    context = "You are a casual zoomer Twitch chat user, chatting with a zoomer streamer. "

    responses = []
    for bot in responding_bots:
        prompt = f"{context} {input_text}"
        response = chatgpt_query(prompt)
        responses.append((bot, response))
    return responses

# Display bot responses
def display_bot_responses(responses):
    for bot, response in responses:
        print(f'{colored(bot.name, bot.color)}: {response}')
        
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

class TransparentChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.chat_label = QTextEdit(self)
        self.chat_label.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_label)
        self.setLayout(layout)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Transparent Chat Window")
        self.setGeometry(100, 100, 400, 600)

    def update_chat(self, bot_name, bot_message, bot_color):
        colored_name = f'<span style="color: {bot_color};">{bot_name}: </span>'
        colored_message = f'<span>{bot_message}</span><br>'
        self.chat_label.insertHtml(colored_name + colored_message)
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