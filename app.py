import streamlit as st
import pipeline
import time

# Helper function to format seconds into HH:MM:SS.ms
def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

# Function to display the 'About' page content from your proposal
def show_about_page():
    st.header("About Textify")
    st.markdown("""
    **Textify** is an AI-based web application that converts YouTube videos into text summaries with timestamps. It is a valuable tool for researchers, content creators, students, and the deaf community.

    ---
    ### **Project Details**
    - **Student Name:** Muhammad Ammar Shahid (STU149433)
    - **Supervisor:** Dr. Nas Yakubu
    - **Course:** RES6011

    ---
    ### **Purpose & Aim**
    The primary objective of this research is to enhance speech-to-text (STT) accuracy in multilingual and noisy environments. We aim to achieve this by fine-tuning AI-based models, leveraging secondary datasets, and optimizing transcription quality with precise timestamping for real-time applications.

    ---
    ### **Novelty**
    This research introduces a fine-tuned STT model optimized for diverse and challenging acoustic conditions. Unlike existing models that rely on generic datasets, this study incorporates targeted noise augmentation and accent adaptation to refine transcription quality. The inclusion of precise timestamp alignment enhances usability for applications requiring real-time processing, bridging the gap between theoretical advancements and practical deployment in speech recognition technology.
    """)

# Main application logic
def main():
    # --- Page Configuration ---
    st.set_page_config(
        page_title="Textify",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="auto"
    )

    # --- Sidebar ---
    with st.sidebar:
        st.title("📝 Textify")
        st.markdown("Your AI-powered tool to transcribe and summarize YouTube videos.")
        st.markdown("---")
        st.info("A project by Muhammad Ammar Shahid")

    # --- Main Page Content ---
    st.title("YouTube Video Summarizer & Transcriber")
    st.markdown("Simply paste a YouTube URL below, and let Textify work its magic. Get a concise summary and a full, timestamped transcript.")

    # --- Input Form ---
    url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("Generate", type="primary"):
        if url:
            with st.spinner("Processing... This may take a few minutes depending on the video length."):
                try:
                    # Run the backend pipeline
                    start_time = time.time()
                    results = pipeline.run_pipeline(url)
                    end_time = time.time()

                    if results:
                        # Store results in session state to persist them
                        st.session_state['summary'] = results['summary']
                        st.session_state['transcript'] = results['transcript']
                        st.session_state['segments'] = results['segments']
                        st.session_state['processing_time'] = end_time - start_time
                        st.success(f"Processing complete in {st.session_state['processing_time']:.2f} seconds!")
                    else:
                        st.error("Failed to process the video. Please check the URL and try again.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a YouTube URL.")

    # --- Display Results ---
    # Check if results exist in the session state before trying to display them
    if 'summary' in st.session_state:
        st.markdown("---")
        st.header("Results")

        # Use tabs for a clean, organized layout
        tab1, tab2, tab3 = st.tabs(["✅ Summary", "📜 Full Transcript", "ℹ️ About this Project"])

        with tab1:
            st.subheader("Generated Summary")
            st.info(st.session_state['summary'])

        with tab2:
            st.subheader("Timestamped Transcript")
            
            # Add a download button for the full transcript
            st.download_button(
                label="Download Transcript (.txt)",
                data=st.session_state['transcript'],
                file_name="transcript.txt",
                mime="text/plain"
            )

            # Display each segment in an expandable section for readability
            for segment in st.session_state['segments']:
                start = format_time(segment['start'])
                end = format_time(segment['end'])
                with st.expander(f"**[{start} -> {end}]** - {segment['text'][:50]}..."):
                    st.write(segment['text'])

        with tab3:
            show_about_page()

if __name__ == "__main__":
    main()