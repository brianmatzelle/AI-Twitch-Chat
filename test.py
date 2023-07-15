import requests

response = requests.get(f'https://chat-tv-api.herokuapp.com/api/v1/generate?model=gpt-3.5-turbo&bot_name=blanc&input_text=hey&streamer_name=james&context=house&memory=nothing')

print(response)