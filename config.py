# config.py
import os

# --- Paths ---
# NOTE: Update FFMPEG_PATH to where you have ffmpeg installed on your system.

OUTPUT_DIR = "data"
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
TRANSCRIPTS_DIR = os.path.join(OUTPUT_DIR, "transcripts")

# --- Models ---
WHISPER_MODEL = "base"
# For better accuracy, you can use "small", "medium", or "large-v3" if your hardware supports it.
# e.g., WHISPER_MODEL = "small"

SUMMARIZER_MODEL = "t5-small"

# --- Summarizer Settings ---
# Max tokens per chunk for the initial summary. t5-small's limit is 512. We use 450 to be safe.
MAX_TOKENS_PER_CHUNK = 450