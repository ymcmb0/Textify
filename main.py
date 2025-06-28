# main.py
from pipeline import run_pipeline
import os
from config import AUDIO_DIR, TRANSCRIPTS_DIR

def main():
    """
    Main function to run the YouTube processing pipeline.
    """
    # Create output directories if they don't exist
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
    
    # --- Get User Input ---
    # For testing, you can uncomment the line below:
    # youtube_url = "https://www.youtube.com/watch?v=1AUJctaLmKE" # Your previous test URL
    youtube_url = input("Enter the YouTube URL you want to summarize: ")
    print(youtube_url)
    if not youtube_url:
        print("No URL provided. Exiting.")
        return

    # --- Run the Pipeline ---
    results = run_pipeline(youtube_url)

    # --- Display Results ---
    if results:
        print("\n" + "="*50)
        print("          PIPELINE COMPLETED SUCCESSFULLY")
        print("="*50 + "\n")
        print("✅ Final Summary:")
        print("----------------")
        print(results['summary'])
        print("\n" + "="*50)
        print(f"📂 Audio file saved at: {results['audio_path']}")
        # The transcript path is constructed for user info, as it's saved in the transcriber
        transcript_filename = os.path.basename(results['audio_path']).split('.')[0] + ".txt"
        print(f"📂 Transcript saved at: {os.path.join(TRANSCRIPTS_DIR, transcript_filename)}")
        print("="*50)

if __name__ == "__main__":
    main()