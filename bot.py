# bot.py
import openai
import random

config = {
    "slang_type": "incel",
    "slang_level": "witty",
    "any_other_notes": "",
}

context = f"You are a casual Twitch.tv chat user, chatting with a livestreamer. You are aware that there are other viewers watching the streamer as well, so speak {config['slang_level']} with {config['slang_type']} slang, and don't make a fool of yourself. Speak concisely. {config['any_other_notes']}"

colors = [
    'red',
    'green',
    'blue',
    # 'yellow',
    'cyan',
    'magenta',
]


class Bot:

    def __init__(self, name):
        self.name = name
        # Memory does have a limit, but it's very high. If the program bugs after a long time using it, just restart it.
        self.memory = [{"role": "system", "content": context}]
        self.color = random.choice(colors)
    
    def createNewMemory(self, who, input_text, name):
        new_memory = {"role": who, "content": input_text, "name": name}
        self.memory.append(new_memory)

    def chatgpt_query(self, input_text, streamer_name, max_tokens=50, temperature=1):
        self.createNewMemory("user", input_text, streamer_name)
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            model="gpt-4",
            messages=self.memory,
            max_tokens=max_tokens,
            # temperature=temperature,
            top_p=1,
        )
        self.createNewMemory("assistant", response.choices[0].message.content, self.name)
        generated_text = response.choices[0].message.content
        return generated_text