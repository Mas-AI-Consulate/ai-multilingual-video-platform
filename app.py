import streamlit as st
import requests
import os
import time
import base64
import google.auth
from google.cloud import translate_v2 as translate
from gtts import gTTS
from googletrans import Translator
import tempfile
from pytube import YouTube
from dotenv import load_dotenv

# 🌍 **Load API Keys Securely**
load_dotenv()
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 🎨 **High-Class UI Styling & Sparkling Cursor**
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #001F3F, #004080, #0080FF);
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.2);
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff8c00, #ff0080);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            box-shadow: 0 4px 10px rgba(255, 255, 255, 0.2);
        }
        .sparkle-cursor {
            position: fixed;
            width: 10px;
            height: 10px;
            background: white;
            border-radius: 50%;
            box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.8);
            pointer-events: none;
            transition: transform 0.2s ease-out;
        }
    </style>
    <script>
        document.addEventListener("mousemove", function(e) {
            var cursor = document.querySelector(".sparkle-cursor");
            if (!cursor) {
                cursor = document.createElement("div");
                cursor.className = "sparkle-cursor";
                document.body.appendChild(cursor);
            }
            cursor.style.left = e.pageX + "px";
            cursor.style.top = e.pageY + "px";
        });
    </script>
    """,
    unsafe_allow_html=True
)

# 🌍 **Language List with Flags**
LANGUAGES = {
    "en": "🇺🇸 English", "es": "🇪🇸 Spanish", "fr": "🇫🇷 French", "de": "🇩🇪 German",
    "zh-CN": "🇨🇳 Chinese", "ar": "🇸🇦 Arabic", "ru": "🇷🇺 Russian", "it": "🇮🇹 Italian",
    "hi": "🇮🇳 Hindi", "ja": "🇯🇵 Japanese", "ko": "🇰🇷 Korean", "pt": "🇧🇷 Portuguese",
    "fa": "🇮🇷 Persian", "la": "🇻🇦 Latin"
}

# 🌟 **Title**
st.markdown("<div class='title'>🌍 Mas-AI Multilingual Video Platform 🚀</div>", unsafe_allow_html=True)

# 📹 **YouTube Video Input**
video_url = st.text_input("📎 Paste YouTube video URL here:", "")

# 📖 **Subtitle & Audio Language Selection**
subtitle_lang = st.selectbox("📜 Subtitle Language", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])
audio_lang = st.selectbox("🔊 Audio Language", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])

# 🚀 **Translate & Play**
if st.button("✨ Translate & Play ✨"):
    if video_url:
        st.success(f"🌟 Fetching video and translating into {LANGUAGES[subtitle_lang]} and {LANGUAGES[audio_lang]}...")
        time.sleep(2)

        # 🎬 **Download YouTube Video**
        yt = YouTube(video_url)
        video_title = yt.title
        video_stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
        video_path = video_stream.download(filename="video.mp4")

        # 📝 **Translate Subtitle**
        translator = Translator()
        translated_text = translator.translate("Hello, how are you?", src="en", dest=subtitle_lang).text
        st.info(f"{LANGUAGES[subtitle_lang]} {translated_text}")

        # 🔊 **Generate Translated Audio**
        tts = gTTS(text=translated_text, lang=audio_lang, slow=False)
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio_file.name)

        # 🎵 **Audio Player**
        audio_base64 = base64.b64encode(open(temp_audio_file.name, "rb").read()).decode()
        st.markdown(f"""
            <audio controls>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

        # 🗑️ **Cleanup**
        os.remove(temp_audio_file.name)

        # 🎥 **Video Player**
        st.video(video_path)

# 🚀 **Powered By**
st.markdown("<div style='text-align: center; margin-top: 30px;'>🚀 Powered by Mas-AI Consulting | Google Cloud Translation API</div>", unsafe_allow_html=True)
