import openai
from chat_window import ChatWindow
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from speech2text import SpeechRecognitionThread
from bots import Bots
from config_window import ConfigWindow

# Default configuration
config = {
    # Streamer configuration
    'streamer_name': '', # Your username on Twitch or YouTube or whatever
    'num_bots': 10,              # Number of bots in your chat
    'bot_update_interval': 10,  # Time in seconds between bot updates (2 seconds)
    'max_num_of_responding_bots': 4, # Max number of bots that can respond to a message at once

    # Chat window configuration
    'chat_font_size': '15px',
    'chat_text_color': 'white',
    'chat_border_color': 'gray',
    'chat_font_weight': '500',

    # OpenAI API configuration
    'openai_api_key': '',

    # Bot configuration
    'bot_config': {
        # Bot configuration
        'streamer_current_action': '', # What you're currently doing (chatting, playing Rocket League, etc.)
        "slang_level": "witty", # The attitude the bots will have (witty, casual, formal)
        "any_other_notes": "", # Any other notes you want to add to the context
        # Each bot will have a random slang type from this list
        'slang_types': [
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
            "incel",
            "normie",
            "chad",
            "goth",
            "emo",
            "hipster",
            "jock",
            "weeb",
            "furry",
            "gamer",
            "programmer",
            "entrepreneur",
            "basketball",
            "football",
            "soccer",
            "baseball",
            "hockey",
            "golf",
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Philadelphia",
            "Atlanta",
            "Detroit",
            "Memphis",
            "Boston",
            "Baltimore",
            "Milwaukee",
            "Canadian",
            "British",
            "Australian",
        ]
    }
}

# Load environment variables
# load_dotenv()
# openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_key = config['openai_api_key']

def user_interface(config, app):
    # Set the application icon
    app_icon = QIcon("./assets/blanc.png")
    app.setWindowIcon(app_icon)

    config['bot_config']['slang_types'].append('internet') # This line fixes a bug, making sure there is always an element in the list (otherwise random() doesn't work)

    print("Chat.tv started. Start talking or type 'exit' to quit.")
    chat_window = ChatWindow(config)
    chat_window.show()

    bots = Bots(config)
    speech_recognition_thread = SpeechRecognitionThread(bots, config)
    speech_recognition_thread.new_response.connect(lambda response: chat_window.update_chat(response[0].name, response[1], response[0].color))
    speech_recognition_thread.start()
    return app.exec()

def main():
    # Create the application
    app = QApplication([])

    config_window = ConfigWindow(config)
    if config_window.exec() == QDialog.Accepted:
        settings = QSettings("blanc_savant", "Chat.tv")
        openai.api_key = settings.value("openai_api_key", "")
        user_interface(config, app)
        

if __name__ == "__main__":
    main()