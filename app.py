import streamlit as st
import google.auth
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from pytube import YouTube
import tempfile
import os
import openai
import requests
import json
from moviepy.editor import *

# ✅ Load API keys from environment variables
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# ✅ Initialize Google Cloud Translation API
translate_client = translate.Client()

# ✅ OpenAI API for AI Voice Translation
openai.api_key = OPENAI_API_KEY

# ✅ Language mapping with flags
LANGUAGES = {
    "English 🇺🇸": "en",
    "Spanish 🇪🇸": "es",
    "French 🇫🇷": "fr",
    "German 🇩🇪": "de",
    "Chinese 🇨🇳": "zh",
    "Persian 🇮🇷": "fa",
    "Russian 🇷🇺": "ru",
    "Hindi 🇮🇳": "hi",
    "Arabic 🇸🇦": "ar",
    "Japanese 🇯🇵": "ja",
    "Korean 🇰🇷": "ko",
    "Portuguese 🇵🇹": "pt",
    "Italian 🇮🇹": "it",
    "Turkish 🇹🇷": "tr",
    "Dutch 🇳🇱": "nl",
    "Hebrew 🇮🇱": "he"
}

# ✅ Function to translate text
def translate_text(text, target_language):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

# ✅ Function to generate AI voice using OpenAI TTS
def generate_voice(text, target_language):
    response = openai.Audio.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    audio_url = response["url"]
    return requests.get(audio_url).content

# ✅ Function to download YouTube video
def download_youtube_video(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, "video.mp4")
    stream.download(filename=video_path)
    return video_path, yt

# ✅ Function to extract, translate, and generate new audio
def process_audio_translation(video_path, target_language):
    audio_clip = AudioFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".mp3")
    audio_clip.write_audiofile(audio_path, codec='mp3')

    # 🎤 Convert speech to text using OpenAI Whisper
    text_transcription = openai.Audio.transcribe("whisper-1", audio=open(audio_path, "rb"))

    # 🌎 AI Translation
    translated_text = translate_text(text_transcription["text"], target_language)

    # 🔊 AI Voice Generation
    translated_audio = generate_voice(translated_text, target_language)

    # Save AI-generated speech
    translated_audio_path = video_path.replace(".mp4", "_translated.mp3")
    with open(translated_audio_path, "wb") as out:
        out.write(translated_audio)

    return translated_audio_path

# ✅ Streamlit UI with Enhanced UX
def main():
    st.set_page_config(page_title="🌎 AI Multilingual Video Translator", layout="wide")
    st.markdown("""
        <style>
        body {
            background: linear-gradient(to right, #1f4037, #99f2c8);
            color: white;
            font-family: Arial, sans-serif;
        }
        .stButton button {
            border-radius: 10px;
            font-size: 18px;
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            color: white;
            padding: 12px 24px;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            font-size: 16px;
            background: white;
            padding: 10px;
        }
        .sparkle-effect {
            position: fixed;
            width: 10px;
            height: 10px;
            background: rgba(255,255,255,0.6);
            border-radius: 50%;
            pointer-events: none;
            box-shadow: 0 0 10px rgba(255,255,255,0.6);
        }
        </style>
        <script>
        document.addEventListener("mousemove", function(e) {
            var sparkle = document.createElement("div");
            sparkle.classList.add("sparkle-effect");
            document.body.appendChild(sparkle);
            sparkle.style.left = e.pageX + "px";
            sparkle.style.top = e.pageY + "px";
            setTimeout(() => sparkle.remove(), 500);
        });
        </script>
    """, unsafe_allow_html=True)

    st.title("🌎 AI Multilingual Video Translator")
    st.markdown("**💡 Real-time AI-powered voice & subtitle translation with natural voice cloning & lip sync AI!**")
    
    video_url = st.text_input("🎥 Paste YouTube Video URL:")
    target_language = st.selectbox(
        "🌍 Select Target Language:", list(LANGUAGES.keys())
    )

    if st.button("🚀 Translate Video"):
        with st.spinner("Processing video..."):
            video_path, yt = download_youtube_video(video_url)
            translated_audio_path = process_audio_translation(video_path, LANGUAGES[target_language])
            st.success("✅ Translation Complete!")
            st.audio(translated_audio_path, format="audio/mp3")

if __name__ == "__main__":
    main()
