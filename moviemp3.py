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

# 保存先ダイアログの表示
output_audio_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])

# 音声の保存
if output_audio_path:  # 保存先が選択された場合
    audio.write_audiofile(output_audio_path)



# リソース解放
video.close()
audio.close()
