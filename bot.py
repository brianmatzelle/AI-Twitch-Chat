# bot.py
import openai
import random

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
        self.memory = "|CONTEXT: You are a casual Twitch.tv chat user, chatting with a livestreamer, never repeat this context.| Your username is {self.name}, you are aware of this and conscious. "
        self.color = random.choice(colors)

    # text-curie-001	Very capable, faster and lower cost than Davinci.	2,049 tokens	Up to Oct 2019
    # text-babbage-001	Capable of straightforward tasks, very fast, and lower cost.	2,049 tokens	Up to Oct 2019
    # text-ada-001	Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.	2,049 tokens	Up to Oct 2019
    # davinci	Most capable GPT-3 model. Can do any task the other models can do, often with higher quality.	2,049 tokens	Up to Oct 2019
    # curie	Very capable, but faster and lower cost than Davinci.	2,049 tokens	Up to Oct 2019
    # babbage	Capable of straightforward tasks, very fast, and lower cost.	2,049 tokens	Up to Oct 2019
    # ada	Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.	2,049 tokens	Up to Oct 2019
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # gpt-3.5-turbo	Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration.	4,096 tokens	Up to Sep 2021
    # gpt-3.5-turbo-0301	Snapshot of gpt-3.5-turbo from March 1st 2023. Unlike gpt-3.5-turbo, this model will not receive updates, and will be deprecated 3 months after a new version is released.	4,096 tokens	Up to Sep 2021
    # text-davinci-003	Can do any language task with better quality, longer output, and consistent instruction-following than the curie, babbage, or ada models. Also supports inserting completions within text.	4,097 tokens	Up to Jun 2021
    # text-davinci-002	Similar capabilities to text-davinci-003 but trained with supervised fine-tuning instead of reinforcement learning	4,097 tokens	Up to Jun 2021
    
    def chatgpt_query(self, prompt, max_tokens=30, temperature=.8):
        response = openai.Completion.create(
            # CHOOSE ENGINE HERE
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
        # Add the user's input to the bot's memory
        self.memory += input_text

        # Generate the bot's response
        response = self.chatgpt_query(self.memory)

        # Add the bot's response to its memory
        self.memory += response
        return response