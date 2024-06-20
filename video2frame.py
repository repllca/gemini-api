import google.generativeai as genai
import time
import glob
from dotenv import load_dotenv
import os
load_dotenv(".env")
#apiキーの読み込み
API_KEY = os.getenv("GEMINI_API_KEY")
#ビデオファイルのパス読み込み
VIDEO_FILE_PATH = os.getenv("VIDEO_FILE_PATH")

video_paths = glob.glob(VIDEO_FILE_PATH+"/*")
print(video_paths)
genai.configure(api_key=API_KEY)
#apiの生成時間
api_time_list = []
start = time.time()
api_request_count = 0
api_time_list.append(start)

for video_path in video_paths:
    end = time.time()
    api_time_list.append(end)
    # time_diff = end-start
    time_diff = end-api_time_list[-2]
    print(time_diff)
    if time_diff <= 120 and api_request_count>=2:
       time.sleep(120-time_diff)
        
    uploaded_video = genai.upload_file(video_path)
    # アップロード完了をチェック
    # `upload_file` は非同期的に実行されるため、完了を待たないと次の処理でエラーが発生してしまう
    while uploaded_video.state.name == "PROCESSING":
        print("Waiting for processed.")
        time.sleep(10)
        uploaded_video = genai.get_file(uploaded_video.name)

    model_name = "models/gemini-1.5-flash-latest"
    model = genai.GenerativeModel(model_name)
    prompt = "動画に映っている動物とその動物が何をしたかをシーン事に説明してください。映像の切り替わりや映っている動物が変わった所をシーンの変わり目とします。これらをcsvファイルの形で出力してください.csvの項目はシーンの開始時間、シーンの終了時間、映っている動物、動物が何をしているかでまとめてください."

    content = [prompt, uploaded_video]
    response = model.generate_content(content)
    print(response.text)
    api_request_count += 1


