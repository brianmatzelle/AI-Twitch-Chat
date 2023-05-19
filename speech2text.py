import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QThreadPool, QRunnable
from time import sleep
import random

class GenerateResponsesWorker(QRunnable):
    def __init__(self, bots, input_text, new_response, chat_window, debug_message, responding_signal):
        super().__init__()
        self.bots = bots
        self.input_text = input_text
        self.new_response = new_response
        self.chat_window = chat_window
        self.debug_message = debug_message
        self.responding_signal = responding_signal

    def run(self):
        self.responding_signal.emit(True)
        bot_responses = self.bots.generate_bot_responses(self.input_text, self.debug_message)
        for bot, response in bot_responses:
            self.new_response.emit((bot, response))
            sleep(random.uniform(0.25, 3))
        self.responding_signal.emit(False)

class SpeechRecognitionThread(QThread):
    new_response = pyqtSignal(object)
    debug_message = pyqtSignal(str)
    listening_signal = pyqtSignal(bool)
    recognizing_signal = pyqtSignal(bool)
    responding_signal = pyqtSignal(bool)
    
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
                worker = GenerateResponsesWorker(self.bots, input_text, self.new_response, self.chat_window, self.debug_message, self.responding_signal)
                self.thread_pool.start(worker)

            sleep(.25)

    # Implement speech-to-text functionality
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            # recognizer.adjust_for_ambient_noise(source)
            self.recognizing_signal.emit(False)
            self.debug_message.emit("Listening...")
            self.listening_signal.emit(True)
            try:
                audio = recognizer.listen(source, timeout=self.config["bot_update_interval"], phrase_time_limit=self.config["bot_update_interval"])
            except sr.WaitTimeoutError:
                self.debug_message.emit("Listening...")
                return ""

        try:
            self.listening_signal.emit(False)
            self.debug_message.emit("Recognizing...")
            self.recognizing_signal.emit(True)
            text = recognizer.recognize_google(audio)
            self.debug_message.emit(f"You said: {text}")
            # self.count = 0
            for _ in range(3):
                if self.count > 0:
                    self.count -= 1
            
            return text
        except Exception as e:
            self.count += 1
            if self.count >= 5:
                if (random.randint(0, 10) < 5) and (len(self.bots.arr) > 1):
                    response = self.bots.remove_random_bot()
                    self.new_response.emit(response)
            self.recognizing_signal.emit(False)
            self.debug_message.emit(f"Error recognizing speech {e}")
            self.listening_signal.emit(True)
            return ""
