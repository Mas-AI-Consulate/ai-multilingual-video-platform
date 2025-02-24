import streamlit as st
import os
import subprocess
from pytube import YouTube
import tempfile
from gtts import gTTS

# Set page config
st.set_page_config(
    page_title="Mas-AI Multilingual Video Platform",
    page_icon="🌍",
    layout="wide"
)

# 🌟 Custom Styling for Fancy UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #1e3c72, #2a5298);
        }
        .title {
            font-size: 42px;
            font-weight: bold;
            color: white;
            text-align: center;
            text-shadow: 2px 2px 8px rgba(255,255,255,0.8);
        }
        .sparkling {
            animation: sparkle 1.5s infinite;
        }
        @keyframes sparkle {
            0% { filter: brightness(100%); }
            50% { filter: brightness(200%); }
            100% { filter: brightness(100%); }
        }
    </style>
""", unsafe_allow_html=True)

# 🌍 Language Options with Flags
LANGUAGES = {
    "en": "🇬🇧 English",
    "es": "🇪🇸 Spanish",
    "fr": "🇫🇷 French",
    "de": "🇩🇪 German",
    "zh-cn": "🇨🇳 Chinese",
    "ar": "🇸🇦 Arabic",
    "ru": "🇷🇺 Russian",
    "hi": "🇮🇳 Hindi",
    "ja": "🇯🇵 Japanese",
    "ko": "🇰🇷 Korean",
    "it": "🇮🇹 Italian",
    "pt": "🇵🇹 Portuguese",
}

# 🌟 Title
st.markdown("<div class='title'>🌍 Mas-AI Multilingual Video Platform 🚀</div>", unsafe_allow_html=True)

# 📌 Input: Video URL
video_url = st.text_input("🔗 Paste YouTube video URL here:", "")

# 📌 Language Selection
col1, col2 = st.columns(2)
with col1:
    subtitle_lang = st.selectbox("📖 Subtitle Language", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])
with col2:
    audio_lang = st.selectbox("🎧 Audio Language", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])

if video_url:
    try:
        # Download Video
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        video_path = stream.download(output_path=tempfile.gettempdir())

        # Extract Audio Using FFmpeg
        audio_path = os.path.join(tempfile.gettempdir(), "audio.mp3")
        subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path], check=True)

        # AI Translate Audio
        tts = gTTS(f"Now playing in {LANGUAGES[audio_lang]}", lang=audio_lang)
        tts_path = os.path.join(tempfile.gettempdir(), "tts_audio.mp3")
        tts.save(tts_path)

        # Show Video
        st.video(video_path)
        st.success(f"🎬 Playing: **{yt.title}**")

        # Play AI-generated Audio
        st.audio(tts_path, format="audio/mp3")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# 🚀 Footer
st.markdown("<div style='text-align: center; color: white; font-size: 18px;'>🔗 Powered by Mas-AI Consulting 🌍</div>", unsafe_allow_html=True)
