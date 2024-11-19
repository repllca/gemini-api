import google.generativeai as genai
import time
import glob
from dotenv import load_dotenv
import os
# load_dotenv(".env")
#apiキーの読み込み
# API_KEY = os.getenv("GEMINI_API_KEY")

API_KEY = ""
#ビデオファイルのパス読み込み

genai.configure(api_key=API_KEY)
#apiの生成時間

image_path = "test.png"
uploaded_video = genai.upload_file(image_path)
# アップロード完了をチェック
# `upload_file` は非同期的に実行されるため、完了を待たないと次の処理でエラーが発生してしまう
while uploaded_video.state.name == "PROCESSING":
    print("Waiting for processed.")
    time.sleep(10)
    uploaded_video = genai.get_file(uploaded_video.name)

model_name = "models/gemini-1.5-flash-latest"
model = genai.GenerativeModel(model_name)
# prompt = "動画に映っている動物とその動物が何をしたかをシーン事に説明してください。映像の切り替わりや映っている動物が変わった所をシーンの変わり目とします。これらをcsvファイルの形で出力してください.csvの項目はシーンの開始時間、シーンの終了時間、映っている動物、動物が何をしているかでまとめてください."
prompt = "成分表示の中身を書き出してください"

content = [prompt, uploaded_video]
response = model.generate_content(content)
print(response.text)

