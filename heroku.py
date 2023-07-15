import requests

def main():
    prompt = "hey how are you?"
    model = "text-davinci-002"
    bot_name = "blanc"
    input_text = "What is your name? I have too many monkeys running around my house!"
    streamer_name = "xQcOW"
    context = "I'm playing Rocket League"
    memory = "I'm playing Rocket League"
    response = generate(prompt, model, bot_name, input_text, streamer_name, context, memory)
    if response:
        print(response)
    else:
        print("An error occurred")


def generate(prompt, model, bot_name, input_text, streamer_name, context, memory):
    # response = requests.get(f'https://chat-tv-api.herokuapp.com/api/v1/generate?prompt={prompt}&model={model}')
    response = requests.get(f'https://chat-tv-api.herokuapp.com/api/v1/generate?prompt={prompt}&model={model}&bot_name={bot_name}&input_text={input_text}&streamer_name={streamer_name}&context={context}&memory={memory}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: received status code {response.status_code}")
        print(f"Response body: {response.text}")
        return None




if __name__ == '__main__':
    main()
