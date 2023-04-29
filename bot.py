# bot.py
import openai
import random
from PyQt5.QtWidgets import QMessageBox, QApplication

class Bot:

    def __init__(self, name, bot_config):
        self.name = name
        self.context = f"You are a casual Twitch.tv chat user, chatting with a livestreamer, currently {bot_config['streamer_current_action']}. You are aware that there are other viewers watching the streamer as well, so speak {bot_config['slang_level']} with {random.sample(bot_config['slang_types'], 1)} slang, and don't make a fool of yourself. Most other viewers speak with different slang. Speak concisely. {bot_config['any_other_notes']}"
        # Memory does have a limit, but it's very high. If the program bugs after a long time using it, just restart it.
        self.memory = [{"role": "system", "content": self.context}]
        self.color = random.choice(colors)
    
    def createNewMemory(self, who, input_text, name):
        new_memory = {"role": who, "content": input_text, "name": name}
        self.memory.append(new_memory)

    def chatgpt_query(self, input_text, streamer_name, max_tokens=50, temperature=1, top_p=1):
        self.createNewMemory("user", input_text, streamer_name)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                # model="gpt-4",
                messages=self.memory,
                max_tokens=max_tokens,
                # temperature=temperature,
                top_p=top_p,
            )
        except openai.error.AuthenticationError as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Error: Invalid API Key")
            error_dialog.setInformativeText("Your API key is incorrect, or you didn't provide one. You can obtain an API key from https://platform.openai.com/account/api-keys.")
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()
            QApplication.instance().quit()
            return

        self.createNewMemory("assistant", response.choices[0].message.content, self.name)
        generated_text = response.choices[0].message.content
        return generated_text

colors = [
    'red',
    'green',
    'blue',
    # 'yellow',
    'cyan',
    'magenta',
]