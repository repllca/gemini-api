"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv(".env")
API_KEY = os.getenv("GEMINI_API_KEY")

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

genai.configure(api_key = API_KEY)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)
#text to textを行う場合
response = chat_session.send_message("what is meaning of life?")

print(response.text)
#video to textを行う場合
# model.gena.GenerativeModel("")