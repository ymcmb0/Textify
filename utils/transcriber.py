# utils/transcriber.py
import whisper
import os
from config import WHISPER_MODEL, TRANSCRIPTS_DIR

def transcribe_audio(audio_path: str) -> dict:
    """
    Transcribes an audio file using Whisper.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        dict: A dictionary containing the full result from Whisper, 
              including 'text' and 'segments'.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at: {audio_path}")

    print(f"[*] Loading whisper model '{WHISPER_MODEL}'...")
    # Consider moving model loading outside if you process many files sequentially
    model = whisper.load_model(WHISPER_MODEL, device="cpu")
    
    print(f"[*] Transcribing audio: {os.path.basename(audio_path)}")
    result = model.transcribe(audio_path, verbose=True, fp16=False) # fp16=False is safer for CPU

    # --- Save the transcript ---
    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    transcript_filename = os.path.basename(audio_path).split('.')[0] + ".txt"
    transcript_path = os.path.join(TRANSCRIPTS_DIR, transcript_filename)
    
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result['text'])
    print(f"[*] Transcript saved to: {transcript_path}")

    return result