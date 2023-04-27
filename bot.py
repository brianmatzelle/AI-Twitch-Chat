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
    'white',
]
class Bot:

    def __init__(self, name):
        self.name = name
        self.memory = ""
        # self.color = self.generate_random_color()
        self.color = random.choice(colors)

    # def generate_random_color(self):
    #     # r = random.randint(0, 255)
    #     # g = random.randint(0, 255)
    #     # b = random.randint(0, 255)
    #     # return f"#{r:02x}{g:02x}{b:02x}"
    #     return random.choice(colors)

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
        context = "You are a casual zoomer Twitch chat user that uses internet slang, chatting with a zoomer streamer. "
        prompt = f"{context} {input_text}"
        response = self.chatgpt_query(prompt)
        return response