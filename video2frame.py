import cv2
import os
import shutil
import google.generativeai as genai

# 環境変数の準備 (左端の鍵アイコンでGOOGLE_API_KEYを設定)

from dotenv import load_dotenv
load_dotenv(".env")
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
# 動画ファイル名
video_file_name = "iputs_video/input1.mp4"

# フォルダの準備
FRAME_EXTRACTION_DIRECTORY = "/content/frames"
FRAME_PREFIX = "_frame"
def create_frame_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

# 動画からのフレーム抽出
def extract_frame_from_video(video_file_path):
    create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
    vidcap = cv2.VideoCapture(video_file_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1 / fps  # フレーム間の時間間隔 (秒単位)
    output_file_prefix = os.path.basename(video_file_path).replace('.', '_')
    frame_count = 0
    count = 0
    while vidcap.isOpened():
        success, frame = vidcap.read()
        if not success: # 動画終了
            break
        if int(count / fps) == frame_count: # 毎秒フレームを抽出
            min = frame_count // 60
            sec = frame_count % 60
            time_string = f"{min:02d}:{sec:02d}"
            image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
            output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
            cv2.imwrite(output_filename, frame)
            frame_count += 1
        count += 1
    vidcap.release() # vidcapの解放
    print("Completed:", frame_count, "frames")

# 動画からのフレーム抽出の実行
extract_frame_from_video(video_file_name)
# Fileクラスの定義
class File:
    def __init__(self, file_path: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
            self.display_name = display_name
        self.timestamp = get_timestamp(file_path)

    def set_file_response(self, response):
        self.response = response

# timestampの取得
def get_timestamp(filename):
    parts = filename.split(FRAME_PREFIX)
    if len(parts) != 2:
        return None
    return parts[1].split('.')[0]

# Fileリストの準備
files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
files = sorted(files)
files_to_upload = []
for file in files:
    files_to_upload.append(
        File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))

# 動画全体をアップロードするかどうか (Falseは10秒のみ)
full_video = False

# ファイルのアップロード
uploaded_files = []
for file in files_to_upload if full_video else files_to_upload[40:50]:
    print(f'Uploading: {file.file_path}...')
    response = genai.upload_file(path=file.file_path)
    file.set_file_response(response)
    uploaded_files.append(file)
# モデルの準備
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# プロンプトの準備
prompt = "この動画を日本語で説明してください。"
request = [prompt]
for file in uploaded_files:
    request.append(file.timestamp) # タイムスタンプ (00:00)
    request.append(file.response) # 静止画フレーム

# 推論の実行
response = model.generate_content(
    request,
    request_options={"timeout": 600} # タイムアウト指定
)
print(response.text) 