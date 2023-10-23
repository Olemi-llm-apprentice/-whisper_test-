import time
from faster_whisper import WhisperModel

start_time = time.time()  # 処理開始時間

# モデルの初期化
model_size = "large-v2"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# 音声ファイルから文字起こし
segments, info = model.transcribe("kosen_001.m4a", beam_size=10)

print(f"Detected language '{info.language}' with probability {info.language_probability}")

# 結果をテキストファイルに保存
with open("transcription.txt", "w") as f:
    for segment in segments:
        f.write(f"[{segment.start}s -> {segment.end}s] {segment.text}\n")
        laptime = time.time() - start_time
        print(f"{laptime}秒経過_[{segment.start}s -> {segment.end}s] {segment.text}")

end_time = time.time()  # 処理終了時間

# 処理時間の計測
elapsed_time = end_time - start_time
print(f"Total time taken: {elapsed_time} seconds")
