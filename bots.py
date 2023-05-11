from bot import Bot
import random
from PyQt5.QtCore import pyqtSignal

class Bots:
    def __init__(self, config, chat_window):
        self.config = config

        # Array of bots
        self.arr = []
        for i in range(config['num_bots']):
            bot = Bot(config['bot_config'], config['streamer_name'])
            chat_window.update_debug(f"{bot.name} has joined the chat!")
            self.arr.append(bot)

    # So bots[i] can be used to access the ith bot in bots.arr
    def __getitem__(self, index):
        return self.arr[index]

    # Generate bot responses
    def generate_bot_responses(self, input_text, debug_message):
        # Determine the number of bots to respond
        if len(self.arr) == 1:
            num_responding_bots = 1
        elif len(self.arr) < self.config["max_num_of_responding_bots"]:
            num_responding_bots = random.randrange(1, len(self.arr)//2)
        else:
            num_responding_bots = random.randrange(1, self.config["max_num_of_responding_bots"])
            
        debug_message.emit(f"Number of bots responding: {num_responding_bots}")
        
        # Randomly select a quarter of the bots
        responding_bots = random.sample(self.arr, num_responding_bots)

        responses = []
        for bot in responding_bots:
            prompt = f"{input_text}"
            response = bot.chatgpt_query(prompt, self.config["streamer_name"].replace(" ", "_"))
            responses.append((bot, response))
        
        # Add/remove bots randomly
        chance = random.randrange(0, 100)
        if chance < 10:
            responses.append(self.add_random_bot())
        elif chance > 90 and len(self.arr) > 1:
            responses.append(self.remove_random_bot())

        return responses

    # Remove a random bot from the array
    def remove_random_bot(self):
        # Remove a random bot
        index = random.randrange(0, len(self.arr))
        bot = self.arr.pop(index)
        msg = f"has left the chat!"
        # print(msg)
        return (bot, msg)
    
    # Add a random bot to the array
    def add_random_bot(self):
        # Add a random bot
        bot = Bot(self.config['bot_config'], self.config['streamer_name'])
        self.arr.append(bot)
        msg = f"has entered the chat!"
        # print(msg)
        return (bot, msg)
    
    def clear_memory(self, chat_window):
        for bot in self.arr:
            bot.clear_memory(chat_window)