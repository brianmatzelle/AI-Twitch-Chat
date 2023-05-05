import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QThreadPool, QRunnable
from time import sleep
import random


class GenerateResponsesWorker(QRunnable):
    def __init__(self, bots, input_text, new_response):
        super().__init__()
        self.bots = bots
        self.input_text = input_text
        self.new_response = new_response

    def run(self):
        bot_responses = self.bots.generate_bot_responses(self.input_text)
        for bot, response in bot_responses:
            self.new_response.emit((bot, response))
            sleep(random.uniform(0.25, 3))


class SpeechRecognitionThread(QThread):
    new_response = pyqtSignal(object)

    def __init__(self, bots, config):
        super().__init__()
        self.bots = bots
        self.config = config
        self.thread_pool = QThreadPool()

    def run(self):
        while True:
            input_text = self.speech_to_text()
            if input_text.lower() == 'exit':
                break

            if input_text.strip():
                worker = GenerateResponsesWorker(self.bots, input_text, self.new_response)
                self.thread_pool.start(worker)

            sleep(.25)

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
