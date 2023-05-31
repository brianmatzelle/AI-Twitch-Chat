import openai
from chat_window import ChatWindow
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from speech2text import SpeechRecognitionThread
from bots import Bots
from config_window import ConfigWindow
# import sys
# if getattr(sys, 'frozen', False):
#     import pyi_splash

# Default configuration
config = {
    # Streamer configuration
    'streamer_name': '', # Your username on Twitch or YouTube or whatever
    'num_bots': 10,              # Number of bots in your chat
    'bot_update_interval': 10,  # Time in seconds between bot updates (2 seconds)
    'max_num_of_responding_bots': 5, # Max number of bots that can respond to a message at once

    # Chat window configuration
    'chat_font_size': '16px',
    'chat_text_color': 'white',
    'chat_border_color': 'rgba(26, 26, 26, 0.9)',
    'chat_font_weight': '500',

    # OpenAI API configuration
    'openai_api_key': '',

    # Bot configuration
    'bot_config': {
        # Bot configuration
        'streamer_current_action': '', # What you're currently doing (chatting, playing Rocket League, etc.)
        "tone": "witty", # The attitude the bots will have (witty, casual, etc.)
        "any_other_notes": "", # Any other notes you want to add to the context
        # Each bot will have a random slang type from this list
        
        'slang_types': [
            "zoomer", "boomer", "twitch chat enthusiast",
            "gen-x", "millenial", "iPad baby",
            "internet", "4chan", "vape fiend",
            "tiktok", "incel", "angry italian american from new jersey",
            "chad", "rocket league", "drunk russian but in broken english",
            "frat", "weeb", "furry that is trying to hide it",
            "Borat", "programmer", "mormon",
            "deadbeat dad", "Joe Rogan fanboy", "QAnon victim",
            "New York", "Los Angeles", "Atlanta rapper who never made it big",
        ],

        'model': "gpt-3.5-turbo"
    }
}

# Load environment variables
openai.api_key = config['openai_api_key'].strip()

def user_interface(config, app):
    # Set the application icon
    app_icon = QIcon("./blanc.png")
    app.setWindowIcon(app_icon)

    # Add an internet slang type if there isn't one
    if len(config['bot_config']['slang_types']) == 0:
        config['bot_config']['slang_types'].append('internet') # This line fixes a bug, making sure there is always an element in the list (otherwise random() doesn't work)

    chat_window = ChatWindow(config)
    chat_window.show()
    bots = Bots(config, chat_window)
    chat_window.assign_bots(bots)
    chat_window.update_debug("\nClick 🐞 to close this menu (debug menu).\n")
    chat_window.update_debug("👂🏼 means the program is listening for your voice.")
    chat_window.update_debug("🤔 means the program is understanding your speech.")
    chat_window.update_debug("🤖💭 means the program is generating a response.\n")
    chat_window.update_chat("Chat.tv started and is listening 👂🏼. Start talking!", "", "gray")
    speech_recognition_thread = SpeechRecognitionThread(bots, config, chat_window)
    speech_recognition_thread.new_response.connect(lambda response: chat_window.update_chat(response[0].name, response[1], response[0].color))
    speech_recognition_thread.debug_message.connect(chat_window.update_debug)
    speech_recognition_thread.listening_signal.connect(chat_window.footer_bar.show_listening)
    speech_recognition_thread.recognizing_signal.connect(chat_window.footer_bar.show_recognizing)
    speech_recognition_thread.responding_signal.connect(chat_window.footer_bar.show_responding)
    speech_recognition_thread.start()
    return app.exec()

def main():
    # # Close the splash screen if this is executed as a frozen app (e.g. pyinstaller)
    # if getattr(sys, 'frozen', False):
    #     pyi_splash.close()  
    # Create the application
    app = QApplication([])

    config_window = ConfigWindow(config)
    config_window.setWindowIcon(QIcon("./blanc.png"))
    if config_window.exec() == QDialog.Accepted:
        settings = QSettings("blanc_savant", "Chat.tv")
        openai.api_key = settings.value("openai_api_key", "")
        user_interface(config, app)
        

if __name__ == "__main__":
    main()