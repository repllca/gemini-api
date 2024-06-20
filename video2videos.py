
import csv
from moviepy.editor import *
i = 0
def makevideo(start,end,video_path,save_path):
    video = VideoFileClip(video_path).subclip(start,end)
    
    video.write_videofile(save_path,fps=29)    # fpsは元の動画に合わせて29に設定
    return video
with open("result/video_split_list.csv",encoding ="utf_8") as f:
    reader = csv.reader(f)
    for row in reader:
        i += 1
        start = row[0]
        end = row[1]
        animal_name = row[2]
        script = row[3]
        save_path = "result/output"+str(i)+".mp4"
        makevideo(start,end,"inputs_video/input1.mp4",save_path)

    
# file_path = "hyokkorihan.mp4"    # 編集したい動画のパス

# start = 19    # 切り出し開始時刻。秒で表現

# end = 24    # 切り出し終了時刻。同じく秒で表現

# save_path = "cat_shiraishi.mp4"    # 編集後のファイル保存先のパス

# video = VideoFileClip(file_path).subclip(start, end)    # ビデオのカット開始

# video.write_videofile(save_path,fps=29)    # fpsは元の動画に合わせて29に設定