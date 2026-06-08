import os
import whisper
import static_ffmpeg
import librosa
import numpy as np
import json

print("Initializing Local AI Environment...")
# Setup ffmpeg so whisper doesn't crash on Windows
static_ffmpeg.add_paths()

audio_file = "song.mp3"

print("--- PHASE 1: AI Beat Detection ---")
print("Analyzing song frequencies to find the heaviest beat drops...")
y, sr = librosa.load(audio_file, sr=None)
# Calculate onset strength (energy spikes)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
# Find peaks
peaks = librosa.util.peak_pick(onset_env, pre_max=7, post_max=7, pre_avg=7, post_avg=7, delta=1.5, wait=20)
# Get the strengths of these peaks
peak_strengths = onset_env[peaks]
# Get the top 40 strongest bass drops in the song
top_indices = np.argsort(peak_strengths)[::-1][:40]
top_peaks = peaks[top_indices]
top_times = sorted(librosa.frames_to_time(top_peaks, sr=sr))

# Format the beat drops array for Javascript
js_beat_drops = "const explicitBeatDrops = [\n    "
js_beat_drops += ", ".join([str(round(t, 2)) for t in top_times])
js_beat_drops += "\n];\n\n"

print("--- PHASE 2: AI Lyric Syncing ---")
print("Loading Whisper AI Base Model (This uses your CPU/GPU, no API key needed!)...")
model = whisper.load_model("base.en")

print("Scanning audio and generating word-level timestamps...")
result = model.transcribe(audio_file, word_timestamps=True)

js_lyrics = "const rawLyrics = [\n"

print("Parsing words...")
for segment in result['segments']:
    for word in segment['words']:
        clean_word = word['word'].replace('"', "'").strip()
        time_sec = round(word['start'], 2)
        if len(clean_word) > 0:
            js_lyrics += f'    {{ time: {time_sec}, text: "{clean_word}" }},\n'

js_lyrics += '    { time: 9999.0, text: "" }\n];'

print("\n--- DONE! JS CODE GENERATED ---\n")
with open("synced_lyrics.js", "w", encoding="utf-8") as f:
    f.write(js_beat_drops + js_lyrics)

print("Check synced_lyrics.js for the exact Javascript code to copy into index.html!")
