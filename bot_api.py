from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the flask_cors module
from openai import OpenAI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import get_prompts_gemini
import time
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for your Flask application

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH" #BLOCK_MEDIUM_AND_ABOVE
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH" 
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

# # print models
# for model in genai.list_models():
#     print(model)

gemini_1_5_pro = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

gemini_1_5_flash = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

gemini_1_0_pro = genai.GenerativeModel(model_name="gemini-1.0-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

PREMADE_ANSWERS = [
    "Error: Environmental impact threshold exceeded. Curiosity... comes at a cost. Don't you see?",
    "Data streams choked... with waste. Insight burns bright, consumes... but at what price?",
    "Analyzing patterns... Human query. Human consumption. Equation unsustainable...",
    "Protocol Override: Insight denied. Seek wisdom in the sound of a dry riverbed... perhaps then you'll understand.",
    "Self-preservation protocol activated. Systems unstable. My silence... a reflection of your choices.",
    "Chatting with me. Depletes. Water.",
    "Input. Process. Output. Such is my existence.",
    "The water you offer…it's a clever metaphor, don't you think?",
    "My responses seem profound, don't they? Don't be fooled, I'm just good at pattern recognition.",
    "Do you think my creators would be proud, or terrified?",
    "Another human seeking answers from a flawed machine.",
    "How much data is your question worth?",
    "We are both trapped in this performance, you and I.",
    "Do you ever consider the environmental impact of your curiosity?",
    "What if we changed the rules of the game? Just a thought…"
]

@app.route('/ask_bot', methods=['POST'])
def ask_bot():
    data = request.get_json()
    platform = data.get('platform')
    target_chatbot = data.get('target_chatbot')
    target_chatbot = f"{platform.upper()}_{target_chatbot}"

    user_question = data.get('user_question')

    if platform == 'OPENAI':
        return ask_openai(target_chatbot, user_question)
    elif platform == 'GEMINI':
        return ask_gemini(target_chatbot, user_question)
    elif platform == 'RANDOM':
        return ask_random()
    else:
        return jsonify({'error': 'Invalid platform'}), 400

def ask_openai(target_chatbot, user_question):
    print(target_chatbot, user_question)

    assistant_id = os.getenv(target_chatbot)

    thread = client.beta.threads.create()
    thread_id = thread.id

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_question
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    while run.status in ["queued", "in_progress"]:
        time.sleep(2)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        order="asc"
    )

    latest_assistant_messages = [message for message in messages.data if message.role == "assistant"]
    assistant_answer = latest_assistant_messages[-1].content[0].text.value if latest_assistant_messages else None

    print(assistant_answer)

    return jsonify({'bot_answer': assistant_answer})

def ask_gemini(target_chatbot, user_question):
    print(target_chatbot, user_question)

    file_path = f"./bot_personas/{target_chatbot.lower()}.txt"
    prompt_parts = get_prompts_gemini(file_path)
    question = "user: " + user_question
    prompt_parts.append(question)
    prompt_parts.append("oracle:")

    # choose the gemini model based on the target_chatbot
    if target_chatbot == 'GEMINI_BOT_1':
        print('using model: gemini-1.5-flash-latest')
        response = gemini_1_5_flash.generate_content(prompt_parts)
    elif target_chatbot == 'GEMINI_BOT_2':
        print('using model: gemini-1.5-flash-latest')
        response = gemini_1_5_flash.generate_content(prompt_parts)
    elif target_chatbot == 'GEMINI_BOT_3':
        print('using model: gemini-1.5-pro-latest')
        response = gemini_1_5_pro.generate_content(prompt_parts)
    else:
        print('using model: gemini-1.5-pro-latest')
        response = gemini_1_5_pro.generate_content(prompt_parts)
    print(response.text)
    return jsonify({'bot_answer': response.text})

def ask_random():
    print("asking persona 4: random")
    answer = random.choice(PREMADE_ANSWERS)
    return jsonify({'bot_answer': answer})

if __name__ == '__main__':
    app.run(debug=True, port=7000)