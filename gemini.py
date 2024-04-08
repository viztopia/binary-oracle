import os
from dotenv import load_dotenv
import json
import google.generativeai as genai

# import the get_prompt_parts function from utils.py
from utils import get_prompts_gemini

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

print("API Key:", GEMINI_API_KEY)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Read prompt parts from input.txt using the get_prompt_parts function
file_path = "./bot_personas/input.txt"
prompt_parts = get_prompts_gemini(file_path)

# Ask a question
question = "What does a more equitable system than capitalism look like?"
question = "user: " + question

# append the question to the prompt parts
prompt_parts.append(question)

# finally, append an empty oracle: to prompt the model to generate a response
prompt_parts.append("oracle:")

print("Prompt Parts:", prompt_parts)

print("sending prompt to model...")
response = model.generate_content(prompt_parts)
print(response.text)

prompt_and_response = "\n".join(prompt_parts) + response.text

# save the prompt plus the response to a file
with open("output.txt", "w") as f:
  f.write(prompt_and_response)