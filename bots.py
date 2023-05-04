from bot import Bot
import random

class Bots:
    def __init__(self, config):
        self.config = config

        # # All possible names for bots
        # self.names = [
        #     'Yeetmaster42', 'VibinCool7', 'LitFam2022', 'SavageSquirrel99', 'KawaiiPenguin24', 'SlayinDragon10',
        #     'BaeWatch69', 'FunkyChicken77', 'SaltyPretzel3', 'BruhMoment88', 'NoCap11', 'YoloSwag2', 'GuacQueen55',
        #     'SickoMode23', 'SavageSzn75', 'VibeCheck12', 'LowkeyLit37', 'HighkeyHype44', 'YoloYoda99',
        #     'FlexinFrida16', 'BigMood93', 'NoChill21', 'FunkyFresh8', 'SquadGoals27', 'CringeKing69', 'MoodSwing55',
        #     'DankDoodle76', 'GucciGorilla62', 'ScreamingPickle18', 'YasYak4', 'LitAF91', 'BaeBison27',
        #     'SlayQueen37', 'SavageSloth22', 'LittyLion5', 'ExtraAF69', 'MemeMachine43', 'Cheechinator69',
        #     'ChillChimp64', 'SickSnek87', 'LitLlama10', 'WildWaffle72', 'WeirdWolf53', 'PhatChicken2002',
        #     'WavyWalrus29', 'SavageShark42', 'HypeHippo58', 'BigMoodBear70', 'DopeDoggo61', 'VibeVulture79',
        #     'ChaosChicken47', 'SickSquid81', 'LittyLemur7', 'CrazyCrab2', 'MemeMoose13', 'SassySasquatch84'
        # ]

        # Array of bots
        self.arr = []
        for i in range(config['num_bots']):
            bot = Bot(config['bot_config'])
            print(f"{bot.name} has joined the chat!")
            self.arr.append(bot)

    # So bots[i] can be used to access the ith bot in bots.arr
    def __getitem__(self, index):
        return self.arr[index]

    # Generate bot responses
    def generate_bot_responses(self, input_text):
        # Determine the number of bots to respond
        num_responding_bots = random.randrange(0, self.config["max_num_of_responding_bots"])
        print(f"Number of bots responding: {num_responding_bots}")
        
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
        elif chance > 90:
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
        bot = Bot(self.config['bot_config'])
        self.arr.append(bot)
        msg = f"has entered the chat!"
        # print(msg)
        return (bot, msg)