import time
import tkinter as tk
from tkinter import filedialog
from faster_whisper import WhisperModel

def main():
    # GUIで音声ファイルを選択
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.m4a")])

    if not file_path:
        print("ファイルが選択されませんでした。終了します。")
        return

    start_time = time.time()  # 処理開始時間

    # モデルの初期化
    model_size = "large-v2"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # 音声ファイルから文字起こし
    segments, info = model.transcribe(file_path, beam_size=10)

    print(f"Detected language '{info.language}' with probability {info.language_probability}")

    # 結果をテキストファイルに保存（タイムスタンプあり）
    with open("transcription_with_timestamp.txt", "w") as f_with_timestamp, open("transcription_without_timestamp.txt", "w") as f_without_timestamp:
        for segment in segments:
            timestamp_text = f"[{segment.start:.0f}s -> {segment.end:.0f}s] {segment.text}\n"
            f_with_timestamp.write(timestamp_text)
            f_without_timestamp.write(f"{segment.text}\n")

            laptime = time.time() - start_time
            print(f"{laptime:.0f}秒経過_{timestamp_text.strip()}")

    end_time = time.time()  # 処理終了時間

    # 処理時間の計測
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.0f} seconds")

if __name__ == "__main__":
    main()
