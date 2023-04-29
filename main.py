import openai
from dotenv import load_dotenv
import os
from chat import ChatWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from speech2text import SpeechRecognitionThread
from bots import Bots

# Default configuration
config = {
    # Streamer configuration
    'streamer_name': 'jit', # Your username on Twitch or YouTube or whatever
    'num_bots': 10,              # Number of bots in your chat
    'bot_update_interval': 10,  # Time in seconds between bot updates (2 seconds)

    # Chat window configuration
    'chat_font_size': '15px',
    'chat_text_color': 'white',
    'chat_border_color': 'gray',
    'chat_font_weight': '500',

    # Bot configuration
    'bot_config': {
        # Bot configuration
        'streamer_current_action': 'Coding a fake live streamer chat in Python', # What you're currently doing (chatting, playing Rocket League, etc.)
        "slang_level": "witty", # The attitude the bots will have (witty, casual, formal)
        "any_other_notes": "", # Any other notes you want to add to the context
        # Each bot will have a random slang type from this list
        'slang_types': [
            "incel",
            "normie",
            "chad",
            "zoomer",
            "boomer",
            "millennial",
            "gen-x",
            "gen-z",
            "gen-alpha",
            "internet",
            "4chan",
            "twitch",
            "tiktok",
            "goth",
            "emo",
            "hipster",
            "jock",
            "emo",
            "weeb",
            "furry",
            "gamer",
            "programmer",
            "developer",
            "politician",
            "businessman",
            "entrepreneur",
            "influencer",
            "basketball",
            "football",
            "soccer",
            "baseball",
            "hockey",
            "golf",
            "new york",
            "los angeles",
            "chicago",
            "houston",
            "philadelphia",
            "atlanta",
            "detroit",
            "memphis",
            "boston",
            "baltimore",
            "milwaukee",
            "Canadian",
            "British",
            "Australian",
            "French",
        ]
    }
}

# Load environment variables
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

def user_interface(config):
    app = QApplication([])

    # Set the application icon
    app_icon = QIcon("./assets/blanc.png")
    app.setWindowIcon(app_icon)

    bots = Bots(config)

    print("Chat.tv started. Start talking or type 'exit' to quit.")
    chat_window = ChatWindow(config)
    chat_window.show()

    speech_recognition_thread = SpeechRecognitionThread(bots, config)
    speech_recognition_thread.new_response.connect(lambda response: chat_window.update_chat(response[0].name, response[1], response[0].color))
    speech_recognition_thread.start()

    app.exec()

def main():
    user_interface(config)

if __name__ == "__main__":
    main()