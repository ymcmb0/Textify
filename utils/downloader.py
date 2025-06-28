# utils/downloader.py
import yt_dlp
import os
import uuid
from config import AUDIO_DIR

def download_audio(youtube_url: str) -> str:
    """
    Downloads audio from a YouTube URL and saves it as an MP3.
    This version pre-defines the output path for robustness.

    Args:
        youtube_url (str): The URL of the YouTube video.

    Returns:
        str: The file path of the downloaded MP3 audio.
    
    Raises:
        Exception: If the download fails.
    """
    # Ensure the output directory exists
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    # 1. Create a unique filename base and define the final MP3 path
    unique_id = uuid.uuid4()
    # We set the output template to the unique ID. yt-dlp will add the original extension.
    output_template = os.path.join(AUDIO_DIR, f"{unique_id}")
    # We know the final path will have the .mp3 extension because of our post-processor.
    final_mp3_path = f"{output_template}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        # NOTE: Add ffmpeg_location here ONLY if it's not in your system PATH
        # 'ffmpeg_location': FFMPEG_PATH, 
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }

    try:
        # 2. Use the simple and robust ydl.download() method
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # 3. Check if the final file exists and return its path
        if os.path.exists(final_mp3_path):
            return final_mp3_path
        else:
            # This is a fallback for a rare case where the original file might have been an mp3
            original_mp3_path = f"{output_template}.mp3"
            if os.path.exists(original_mp3_path):
                return original_mp3_path
            raise FileNotFoundError(f"FFmpeg post-processing failed. Expected MP3 not found at {final_mp3_path}")

    except Exception as e:
        print(f"Error during download or processing: {e}")
        raise