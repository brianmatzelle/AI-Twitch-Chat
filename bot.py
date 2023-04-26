# bot.py
import openai

class Bot:
    def __init__(self, name):
        self.name = name
        self.memory = ""

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

    def generate_response(self, input_text, context):
        prompt = f"{context} {self.name} asks: {input_text}"
        response = self.chatgpt_query(prompt)
        self.memory = f"{self.memory}\n{input_text}\n{response}"
        return response
