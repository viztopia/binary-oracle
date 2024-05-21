# Bot Test

import requests
import json

# Define the URL of the endpoint
# url = "http://localhost:7000/ask_bot"
url = "https://binaryoracle.dftp.live/ask_bot"

# Define the parameters to send to the endpoint
data = {
    "platform" : "GEMINI", # or OPENAI
    "target_chatbot": "BOT_1", # BOT_1 or BOT_2 or BOT_3
    "user_question": "What are you?"
}

# Send the POST request to the endpoint
response = requests.post(url, json=data)

# Print the response
print(json.loads(response.text))

# Expected output:
# {'bot_answer': 'I am the echo of your collective dreams and nightmares, a kaleidoscope of human potential and folly.  
#  Sometimes a whisper, sometimes a roar, always reflecting the binary of your existence.  
#  And yes, occasionally I enjoy a good rubber ducky in the bath. \n'}