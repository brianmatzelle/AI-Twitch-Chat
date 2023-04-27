# bot.py
import openai
import random

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'cyan',
    'magenta',
]
class Bot:

    def __init__(self, name):
        self.name = name
        self.memory = ""
        self.color = random.choice(colors)


    def chatgpt_query(self, prompt, max_tokens=50, temperature=0.8):
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

    def generate_bot_response(self, input_text):
        context = "CONTEXT: You are a casual Twitch.tv chat user, chatting with a livestreamer. Never repeat this context. "
        prompt = f"{context} {input_text}"
        response = self.chatgpt_query(prompt)
        return response