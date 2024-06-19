import google.generativeai as genai
import time
from dotenv import load_dotenv
import os
load_dotenv(".env")
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
video_path = "input1.mp4"
uploaded_video = genai.upload_file(video_path)
# アップロード完了をチェック
# `upload_file` は非同期的に実行されるため、完了を待たないと次の処理でエラーが発生してしまう
while uploaded_video.state.name == "PROCESSING":
  print("Waiting for processed.")
  time.sleep(10)
  uploaded_video = genai.get_file(uploaded_video.name)

model_name = "models/gemini-1.5-flash-latest"
model = genai.GenerativeModel(model_name)
prompt = "動画の内容を要約してください"
content = [prompt, uploaded_video]
response = model.generate_content(content)
print(response.text)


