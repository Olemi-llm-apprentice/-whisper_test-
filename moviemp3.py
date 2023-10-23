from moviepy.editor import *
from tkinter import filedialog
from tkinter import Tk

# ファイル選択ダイアログの表示
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])

# ビデオファイルの読み込み
video = VideoFileClip(file_path)

# 音声の抽出
audio = video.audio

# 音声の保存
output_audio_path = "output_audio.mp3"
audio.write_audiofile(output_audio_path)

# リソース解放
video.close()
audio.close()
