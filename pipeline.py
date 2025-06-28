# pipeline.py
from utils.downloader import download_audio
from utils.transcriber import transcribe_audio
from utils.summarizer import summarize_transcript
import os

def run_pipeline(url: str) -> dict:
    """
    Runs the full pipeline: Download -> Transcribe -> Summarize.

    Args:
        url (str): The YouTube URL to process.

    Returns:
        dict: A dictionary containing the results, including summary and transcript segments.
    """
    try:
        print("\n[*] 1. Downloading audio...")
        audio_path = download_audio(url)
        print(f"[+] Audio downloaded successfully: {audio_path}")

        print("\n[*] 2. Transcribing audio...")
        transcription_result = transcribe_audio(audio_path)
        transcript_text = transcription_result['text']
        # *** NEW: Get the segments for timestamped transcript ***
        transcript_segments = transcription_result['segments']
        print("[+] Transcription complete.")

        print("\n[*] 3. Summarizing transcript...")
        summary = summarize_transcript(transcript_text)
        print("[+] Summarization complete.")
        
        return {
            "audio_path": audio_path,
            "transcript": transcript_text,
            "summary": summary,
            "segments": transcript_segments  # <-- Return the segments
        }

    except FileNotFoundError as e:
        print(f"\n[ERROR] A file was not found: {e}")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred in the pipeline: {e}")
    
    return None