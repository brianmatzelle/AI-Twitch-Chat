import speech_recognition as sr
import openai
import random
import tkinter as tk
import math
import string
from bot import Bot

# Replace 'your_openai_api_key' with your actual OpenAI API key
openai.api_key = "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"

# Default configuration
config = {
    'num_bots': 5,
    'bot_update_interval': 2000,  # Time in milliseconds between bot updates (5000 = 5 seconds)
    # Add other settings here as needed
}

ZOOMER_NAMES = [
    'Yeetmaster42', 'VibinCool7', 'LitFam2022', 'SavageSquirrel99', 'KawaiiPenguin24', 'SlayinDragon10',
    'BaeWatch69', 'FunkyChicken77', 'SaltyPretzel3', 'BruhMoment88', 'NoCap11', 'YoloSwag2', 'GuacQueen55',
    'SickoMode23', 'SavageSzn75', 'VibeCheck12', 'LowkeyLit37', 'HighkeyHype44', 'YoloYoda99',
    'FlexinFrida16', 'BigMood93', 'NoChill21', 'FunkyFresh8', 'SquadGoals27', 'CringeKing69', 'MoodSwing55',
    'DankDoodle76', 'GucciGorilla62', 'ScreamingPickle18', 'YasYak4', 'LitAF91', 'BaeBison27',
    'SlayQueen37', 'SavageSloth22', 'LittyLion5', 'ExtraAF69', 'MemeMachine43', 'RadRaven99',
    'ChillChimp64', 'SickSnek87', 'LitLlama10', 'WildWaffle72', 'WeirdWolf53', 'FunkyFerret31',
    'WavyWalrus29', 'SavageShark42', 'HypeHippo58', 'BigMoodBear70', 'DopeDoggo61', 'VibeVulture79',
    'ChaosChicken47', 'SickSquid81', 'LittyLemur7', 'CrazyCrab2', 'MemeMoose13', 'SassySasquatch84'
]
# List of colors
COLORS = ['red', 'green', 'blue', 'orange', 'purple', 'pink', 'yellow', 'black']

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

class TransparentChatWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the desired width and height
        window_width = int(screen_width / 10)
        window_height = int(screen_height * 2 / 3)

        # Set the window size
        self.geometry(f"{window_width}x{window_height}")

        self.configure(bg="white", highlightthickness=0)
        self.wm_attributes("-alpha", 1)  # Adjust the transparency (0 to 1), set to 1 for fully transparent
        self.wm_attributes("-topmost", 0)  # Keep the window on top

        self.chat_text = tk.StringVar()
        self.chat_label = tk.Label(self, textvariable=self.chat_text, font=("Arial", 12), bg="white", wraplength=window_width)
        self.chat_label.pack(padx=10, pady=10, fill="both", expand=True)
        self.chat_label.configure(bg="SystemButtonFace", highlightthickness=0)  # Set the text background to fully transparent 

    def update_chat(self, text):
        current_text = self.chat_text.get()
        self.chat_text.set(f"{current_text}\n{text}")

# Set up the environment
def setup_environment():
    pass

# Connect to ChatGPT API
def connect_chatgpt_api():
    pass

# Implement speech-to-text functionality
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except Exception as e:
        print("Error recognizing speech:", e)
        return ""

# Create bot users
def create_bot_users():
    num_bots = config['num_bots']
    bots = []
    for i in range(num_bots):
        bot_name = f"{random_name()}"
        bots.append(bot_name)
    return bots

# Generate random bot names
def random_name(length=5):
    return random.choice(ZOOMER_NAMES)

# Handle incoming messages
def process_input(input_text):
    # Extract relevant information or context from the input
    return input_text


# Generate bot responses
def generate_bot_responses(input_text, bots):
    # Determine the number of bots to respond
    num_responding_bots = math.ceil(len(bots) / 4)

    # Randomly select a quarter of the bots
    responding_bots = random.sample(bots, num_responding_bots)

    # Add a context for casual Twitch chat
    context = "You are a casual zoomer Twitch chat user, chatting with a zoomer streamer. "

    responses = []
    for bot in responding_bots:
        prompt = f"{context} {input_text}"
        response = chatgpt_query(prompt)
        responses.append((bot, response))
    return responses


def display_bot_responses(responses, chat_window):
    for bot, response in responses:
        min_delay = 500  # Minimum delay in milliseconds
        max_delay = 3000  # Maximum delay in milliseconds
        delay = random.randint(min_delay, max_delay)  # Random delay between min_delay and max_delay

        # Schedule each bot response to be displayed after a random delay
        chat_window.after(delay, lambda bot=bot, response=response: chat_window.update_chat(f"{bot}: {response}"))

# Implement user interface
def user_interface(chat_window):
    bots = create_bot_users()

    print("Chat.tv started. Start talking or type 'exit' to quit.")

    def schedule_update_ui():
        update_interval = config['bot_update_interval']
        chat_window.after(update_interval, update_ui)  # Schedule the update_ui() function to run after the configured interval

    def update_ui():
        input_text = speech_to_text()
        if input_text.lower() == 'exit':
            chat_window.destroy()  # Close the chat window when exiting
            return

        # Only process input and generate bot responses if input_text is not empty
        if input_text.strip():
            processed_input = process_input(input_text)
            bot_responses = generate_bot_responses(processed_input, bots)
            display_bot_responses(bot_responses, chat_window)

        schedule_update_ui()  # Schedule the next update

    schedule_update_ui()  # Start the update loop

def main():
    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Create transparent chat window
    chat_window = TransparentChatWindow(root)

    # Set up environment and run the user interface
    setup_environment()
    user_interface(chat_window)

    # Start the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
