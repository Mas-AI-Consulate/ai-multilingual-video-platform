import streamlit as st
import google.auth
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from pytube import YouTube
import tempfile
import os
import openai
import subprocess
from video_processor import process_video_translation, sync_lips

# Load API keys
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GOOGLE_TTS_API_KEY = os.getenv("GOOGLE_TTS_API_KEY")

# Set up Google Cloud Translation API
translate_client = translate.Client()
openai.api_key = OPENAI_API_KEY

# Streamlit UI
def main():
    st.set_page_config(page_title="AI Multilingual Video Translator", layout="wide")
    st.markdown(
        "<h1 style='text-align: center; color: #ff9900;'>🌎 AI Multilingual Video Translator</h1>",
        unsafe_allow_html=True
    )
    st.markdown("**Translate voice & subtitles in real time with AI!**")

    video_url = st.text_input("🎥 Paste YouTube Video URL:")
    target_language = st.selectbox(
        "🌍 Select Target Language:",
        ["en", "es", "fr", "de", "zh", "fa", "ru", "hi", "ja", "ko", "pt", "it", "ar", "tr"]
    )

    if st.button("🚀 Translate Video"):
        with st.spinner("Processing video..."):
            video_path, yt = download_youtube_video(video_url)
            translated_video = process_video_translation(video_path, target_language)

            st.success("Translation Complete! 🎉")
            st.video(translated_video)

if __name__ == "__main__":
    main()
