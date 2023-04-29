# Description: This file contains the SpeechRecognitionThread class which is a 
# thread that listens for user input and converts it to text.
import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal

class SpeechRecognitionThread(QThread):
    new_response = pyqtSignal(object)

    def __init__(self, bots, config):
        super().__init__()
        self.bots = bots
        self.config = config

    def run(self):
        while True:
            input_text = self.speech_to_text()
            if input_text.lower() == 'exit':
                break

            if input_text.strip():
                bot_responses = self.bots.generate_bot_responses(input_text)
                for bot, response in bot_responses:
                    self.new_response.emit((bot, response))

    # Implement speech-to-text functionality
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=self.config["bot_update_interval"], phrase_time_limit=self.config["bot_update_interval"])
            except sr.WaitTimeoutError:
                print("Timeout while waiting for user input. Listening again...")
                return ""

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except Exception as e:
            print("Error recognizing speech:", e)
            return ""