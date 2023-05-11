import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QThreadPool, QRunnable
from time import sleep
import random

class GenerateResponsesWorker(QRunnable):
    def __init__(self, bots, input_text, new_response, chat_window, debug_message):
        super().__init__()
        self.bots = bots
        self.input_text = input_text
        self.new_response = new_response
        self.chat_window = chat_window
        self.debug_message = debug_message

    def run(self):
        bot_responses = self.bots.generate_bot_responses(self.input_text, self.debug_message)
        for bot, response in bot_responses:
            self.new_response.emit((bot, response))
            sleep(random.uniform(0.25, 3))

class SpeechRecognitionThread(QThread):
    new_response = pyqtSignal(object)
    debug_message = pyqtSignal(str)
    
    def __init__(self, bots, config, chat_window):
        super().__init__()
        self.bots = bots
        self.config = config
        self.thread_pool = QThreadPool()
        self.count = 0
        self.chat_window = chat_window

    def run(self):
        while True:
            input_text = self.speech_to_text()
            if input_text.lower() == 'exit':
                break

            if input_text.strip():
                worker = GenerateResponsesWorker(self.bots, input_text, self.new_response, self.chat_window, self.debug_message)
                self.thread_pool.start(worker)

            sleep(.25)

    # Implement speech-to-text functionality
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.debug_message.emit("Listening...")
            try:
                audio = recognizer.listen(source, timeout=self.config["bot_update_interval"], phrase_time_limit=self.config["bot_update_interval"])
            except sr.WaitTimeoutError:
                self.debug_message.emit("Listening...")
                return ""

        try:
            self.debug_message.emit("Recognizing...")
            text = recognizer.recognize_google(audio)
            self.debug_message.emit(f"You said: {text}")
            # self.count = 0
            if self.count > 0:
                self.count -= 1
                if self.count > 0:
                    self.count -= 1
            
            return text
        except Exception as e:
            self.count += 1
            if self.count >= 5:
                if (random.randint(0, 10) < 5) and (len(self.bots.arr) > 1):
                    self.bots.remove_random_bot()
            self.debug_message.emit(f"Error recognizing speech, {e}")
            return ""
