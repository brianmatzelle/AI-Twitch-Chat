# bot.py
import openai
import random
from PyQt5.QtWidgets import QMessageBox, QApplication
import time
import requests
from random_username.generate import generate_username

MAX_RETRIES = 3
RETRY_DELAY = 2

# # Twitch slang
twitch_slang = [
    'pog', 'KEKW', 'kappa', 'pogchamp', 'pogU', 'LUL', 'monkaS', 
    'poggers', 'slatt', 'jebaited', 'F', 'PepeLaugh',
    'L', 'L', 'L', 'L', 'W', 'W', 'W', 'W', 
    'gas', 'hype', 'mald', 'FeelsBadMan', 'sadge'
]

# # All possible names for bots
usernames = [
    'Yeetmaster42', 'VibinCool7', 'LitFam2022', 'SavageSquirrel99', 'KawaiiPenguin24', 'SlayinDragon10',
    'BaeWatch69', 'FunkyChicken77', 'SaltyPretzel3', 'BruhMoment88', 'NoCap11', 'YoloSwag2', 'GuacQueen55',
    'SickoMode23', 'SavageSzn75', 'VibeCheck12', 'LowkeyLit37', 'HighkeyHype44', 'YoloYoda99',
    'FlexinFrida16', 'BigMood93', 'NoChill21', 'FunkyFresh8', 'SquadGoals27', 'CringeKing69', 'MoodSwing55',
    'DankDoodle76', 'GucciGorilla62', 'ScreamingPickle18', 'YasYak4', 'LitAF91', 'BaeBison27',
    'SlayQueen37', 'SavageSloth22', 'LittyLion5', 'ExtraAF69', 'MemeMachine43', 'Cheechinator69',
    'ChillChimp64', 'SickSnek87', 'LitLlama10', 'WildWaffle72', 'WeirdWolf53', 'PhatChicken2002',
    'WavyWalrus29', 'SavageShark42', 'HypeHippo58', 'BigMoodBear70', 'DopeDoggo61', 'VibeVulture79',
    'ChaosChicken47', 'SickSquid81', 'LittyLemur7', 'CrazyCrab2', 'MemeMoose13', 'SassySasquatch84',
    "ChonkyBodegaCat72", "DeadassPythonista15", "Yo-SeltzerSippa88", "BrooklynBopBuddy03", "LittyLongIsland29",
    "Yerrr-CodeSlanger42", "SchmoodSwingScripter66", "5BoroDebugga", "VaxxBodegaBaby54", "MegaMindMensch99",
    "BiggieBytes47", "GucciGowanus21", "LtrainLunatic-89", "HennyHacka33", "BeefPattyBoosta76",
    "AstoriaAlgorithm07", "CodeConeyIsland90", "LobstaRollLovah12", "BennyBixOyster38", "SohoSyntax17", 
    "RamenRatKing59", "PizzaRatProgramma81", "TimesSquareTechie11", "TimsTinkering29", "BamboozlinBronx50",
    "BagelBodegaBandit23", "NoSleepTilBrooklyn", "SubwaySurfinScript19", "Jawnz-Jupyter44", "DumboDebugger75",
    "CanarsieCoder67", "HarlemHelloWorld92", "JsInJamaica58", "QueensQuirks34", "StatenIslandSnark83",
    "FerryFunky05", "WilliamsburgWhiz40", "MetsMistakeMaker32", "YankeeDoodleDandy68", "NotoriousAInyc",
    "HotdogHallOfFamer79", "NoCapCentralPark87", "EmpireStateEnergizer28", "EastVillageVibez49", "FlatbushFunkyFresh26",
    "ManhattanMemeMasta61", "PythonPicklePals16", "UptownUnicorn22", "DowntownDaredevil09", "OffWhiteWallSt77",
    "NeonNolita65", "TribecaTroll55", "ChelseaChatter43", "WackyWashington30", "KookyKatzDeli64",
    "LESLoopy52", "GowanusGuru18", "CrownHeightsCraze96", "BayRidgeBashful13", "GreenpointGiggles71",
    "ParkSlope-Pixie39", "BushwickBuddy08", "RedHookRascal31", "ProspectParkPunster48", "BotanicalBants37",
    "ConeyIslandClown14", "RockawayRuckus78", "UnisphereUnicorn94", "FlushingFunky46", "ChinatownChaos45",
    "LittleItalyLOL69", "MidtownMischief35", "HellsKitchenHilarity86", "GarmentGuffaws63", "TheaterDistrictThrills24",
    "HudsonYardsHoots10", "FiDiFunnies27", "BatteryParkBellylaughs80", "GramercyGiggler60", "MurrayHillMadness41",
    "KipsBayKook56", "EastHarlemHumor53", "UpperEastSideUproar62", "UESUncontrollable85", "UpperWestSideWhimsy74",
    "UWSUnstoppable25", "InwoodInsanity36", "WashingtonHeightsWit57", "WHWonka91", "BlockSpinna4",
    "b0tB0i", "BotB0iiiiii", "bodegaShawty2001", "bodegaBaddie2002", "treeeeeesha12",
    "dawgDaddy", "fuxWitMe06", "fuxWitMe07", "fuxWitMe08", "BlocccHitta99",
    "xXx_fireFlameSpitta_xXx", "xXx_420blazeit_xXx", "xXx_dankDoodle_xXx", "theGNB", "xxSWATZOMBIExx",
    "BeanrBoi3", "LilPeepPhan", "gamerGurl420", "sickoMode23", "savageSzn75", "wtwOnGod",
    "littyLion5", "extraAF69", "memeMachine43", "cheechinator69", "chillChimp64", "sickSnek87"
    "zaddyQuazar", "KweenKaddyKop", "Po-poPapi", "fudgePacker", "daddyDong", "daddyDonger", "daddyDongest",
    "b1gPapiC", "homeboi_latto", "chulaChinga14", "wackazzShifta", "dull_pnk", "electric",
    "lego_boyf19", "rubenwarrior38", "bnug242", "baseball_1219", "Fluofy", "@drove", "HIVaids",
    "ashleybda", "ZERUSSIANGUY", "whettaM", "swagamuffin", "mercury", "cheeky_nandos20",
]

class Bot:

    def __init__(self, bot_config, streamer_name):
        # self.name = generate_username(1)[0]
        self.name = random.choice(usernames)
        self.context = f"""
        CONTEXT:
        You're a Twitch.tv chat user, chatting with a streamer who is {bot_config['streamer_current_action']}. 
        You're aware that there are other real people watching the streamer, whos name is {streamer_name}. 
        Your tone is {bot_config['tone']}. 
        Your personality is {random.sample(bot_config['slang_types'], 1)}. 
        If you're confused say {random.sample(twitch_slang, 1)}.
        Less than a sentence. 
        END CONTEXT.
        """
        #@DAVINCI@# self.context = f"CONTEXT: You are a Twitch.tv chat user, chatting with a livestreamer who is {bot_config['streamer_current_action']}. Other viewers are also watching the streamer, {bot_config['tone']} is your tone. Resond with less than a sentence, taking max 2 words from this list: {twitch_slang}."
        # Memory does have a limit, but it's very high. If the program bugs after a long time using it, just restart it.
        self.memory = [{"role": "system", "content": self.context}]
        self.color = random.choice(colors)
        self.bot_config = bot_config
    
    def createNewMemory(self, who, input_text, name):
        new_memory = {"role": who, "content": input_text, "name": name}
        self.memory.append(new_memory)

    def clear_memory(self, chat_window):
        self.memory = [{"role": "system", "content": self.context}]
        chat_window.update_debug(f"{self.name}'s memory has been cleared.")

    def chatgpt_query(self, input_text, streamer_name, debug_signal):
        if self.bot_config['model'] == 'gpt-3.5-turbo' or self.bot_config['model'] == 'gpt-4':
            self.createNewMemory("user", input_text, streamer_name)

        for _ in range(MAX_RETRIES):
            try:
                response = requests.get(f'https://chat-tv-api.herokuapp.com/api/v1/generate?model={self.bot_config["model"]}&bot_name={self.name}&input_text={input_text}&streamer_name={streamer_name}&context={self.context}&memory={self.memory}')
            except:
                debug_signal.emit("An error with the API occurred, returning None.")
                return None

            if response.status_code == 200:
                if "Error: Invalid API Key" in response.json():
                    debug_signal.emit("Error: Invalid API Key")
                    time.sleep(RETRY_DELAY)
                if "The rate limit for API requests has been exceeded. The program will wait for some time and retry." in response.json():
                    debug_signal.emit("The rate limit for API requests has been exceeded. The program will wait for some time and retry.")
                    time.sleep(RETRY_DELAY)
                return response.json()
            else:
                debug_signal.emit(f"Error: received status code {response.status_code}")
                debug_signal.emit(f"Response body: {response.text}")
                return None

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'cyan',
    'magenta',
]