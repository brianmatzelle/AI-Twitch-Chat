from bot import Bot
import random
import math

class Bots:
    def __init__(self, config):
        self.config = config
        self.size = config['num_bots']

        # All possible names for bots
        self.names = [
            'Yeetmaster42', 'VibinCool7', 'LitFam2022', 'SavageSquirrel99', 'KawaiiPenguin24', 'SlayinDragon10',
            'BaeWatch69', 'FunkyChicken77', 'SaltyPretzel3', 'BruhMoment88', 'NoCap11', 'YoloSwag2', 'GuacQueen55',
            'SickoMode23', 'SavageSzn75', 'VibeCheck12', 'LowkeyLit37', 'HighkeyHype44', 'YoloYoda99',
            'FlexinFrida16', 'BigMood93', 'NoChill21', 'FunkyFresh8', 'SquadGoals27', 'CringeKing69', 'MoodSwing55',
            'DankDoodle76', 'GucciGorilla62', 'ScreamingPickle18', 'YasYak4', 'LitAF91', 'BaeBison27',
            'SlayQueen37', 'SavageSloth22', 'LittyLion5', 'ExtraAF69', 'MemeMachine43', 'Cheechinator69',
            'ChillChimp64', 'SickSnek87', 'LitLlama10', 'WildWaffle72', 'WeirdWolf53', 'PhatChicken2002',
            'WavyWalrus29', 'SavageShark42', 'HypeHippo58', 'BigMoodBear70', 'DopeDoggo61', 'VibeVulture79',
            'ChaosChicken47', 'SickSquid81', 'LittyLemur7', 'CrazyCrab2', 'MemeMoose13', 'SassySasquatch84'
        ]

        # Array of bots
        self.arr = []
        for i in range(self.size):
            bot = Bot(random.choice(self.names), config['bot_config'])
            self.arr.append(bot)

    # So bots[i] can be used to access the ith bot in bots.arr
    def __getitem__(self, index):
        return self.arr[index]

    # Generate bot responses
    def generate_bot_responses(self, input_text):
        # Determine the number of bots to respond
        max_responding_bots = math.ceil(self.size) / 2 if self.size > 1 else 1
        num_responding_bots = random.randrange(0, max_responding_bots)

        # Randomly select a quarter of the bots
        responding_bots = random.sample(self.arr, num_responding_bots)

        responses = []
        for bot in responding_bots:
            prompt = f"{input_text}"
            response = bot.chatgpt_query(prompt, self.config["streamer_name"])
            responses.append((bot, response))
        return responses