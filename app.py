import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
from gtts import gTTS
import tempfile
import os
import base64

# Set page config for a fancy UI
st.set_page_config(
    page_title="Mas-AI Multilingual Player 🌍",
    page_icon="🌟",
    layout="wide"
)

# 🎨 Custom CSS for fancy UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #1e3c72, #2a5298);
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background: linear-gradient(45deg, #1a2a6c, #b21f1f, #fdbb2d);
            animation: gradientBG 15s ease infinite;
            background-size: 400% 400%;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .stTextInput, .stSelectbox, .stButton>button {
            border-radius: 10px !important;
            font-size: 18px;
        }
        .title {
            font-size: 42px;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 8px rgba(255,255,255,0.5);
            text-align: center;
        }
        .glow-cursor {
            position: fixed;
            width: 15px;
            height: 15px;
            background: radial-gradient(circle, #ff0, #f00);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            animation: sparkle 1.5s infinite;
        }
        @keyframes sparkle {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
    <div class="glow-cursor" id="glowCursor"></div>
    <script>
        document.addEventListener("mousemove", function(event) {
            var cursor = document.getElementById("glowCursor");
            cursor.style.left = event.clientX + "px";
            cursor.style.top = event.clientY + "px";
        });
    </script>
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
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        video_path = stream.download(output_path=tempfile.gettempdir())

        st.video(video_path)
        st.success(f"🎬 Playing: **{yt.title}**")

        # 🎤 Generate AI Audio Translation (Example using gTTS)
        text = f"This video is being translated into {LANGUAGES[audio_lang]}"
        tts = gTTS(text=text, lang=audio_lang)
        audio_path = os.path.join(tempfile.gettempdir(), "translated_audio.mp3")
        tts.save(audio_path)

        st.audio(audio_path, format="audio/mp3")

        # 🌍 Display Selected Languages & Flags
        st.markdown(f"🎭 **Audio:** {LANGUAGES[audio_lang]} | 📖 **Subtitles:** {LANGUAGES[subtitle_lang]}")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# 🚀 Footer
st.markdown("<div style='text-align: center; color: white; font-size: 18px;'>🔗 Powered by Mas-AI Consulting 🌍</div>", unsafe_allow_html=True)
