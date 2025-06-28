# utils/summarizer.py
from transformers import pipeline
from config import SUMMARIZER_MODEL, MAX_TOKENS_PER_CHUNK

# Load the model once when the module is imported
print("[*] Loading summarization model...")
summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
print("[*] Summarization model loaded.")

def _chunk_text(text: str) -> list[str]:
    """Splits the text into chunks of a specified size."""
    words = text.split()
    return [" ".join(words[i:i + MAX_TOKENS_PER_CHUNK]) for i in range(0, len(words), MAX_TOKENS_PER_CHUNK)]

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes the transcript using a two-stage process.
    1. Summarize individual chunks.
    2. Combine chunk summaries and summarize again for a final, coherent summary.

    Args:
        transcript_text (str): The full text of the transcript.

    Returns:
        str: The final, coherent summary.
    """
    if not transcript_text.strip():
        return "The transcript was empty, no summary could be generated."

    chunks = _chunk_text(transcript_text)
    
    print(f"[*] Generating summary from {len(chunks)} chunk(s)...")
    
    # Stage 1: Summarize each chunk
    chunk_summaries = summarizer(
        chunks, 
        max_length=150, 
        min_length=30, 
        do_sample=False
    )
    
    intermediate_summary = "\n".join([summary['summary_text'] for summary in chunk_summaries])

    # Stage 2: If we have multiple chunks, summarize the combined summaries
    if len(chunks) > 1:
        print("[*] Consolidating summary...")
        final_summary_list = summarizer(
            intermediate_summary,
            max_length=250, # Allow for a longer final summary
            min_length=50,
            do_sample=False
        )
        final_summary = final_summary_list[0]['summary_text']
    else:
        final_summary = intermediate_summary

    return final_summary