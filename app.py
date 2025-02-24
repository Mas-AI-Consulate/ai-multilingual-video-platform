import streamlit as st
from pytube import YouTube
import requests
import os
from moviepy.editor import *
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Mas-AI Multilingual Platform 🌍", layout="centered")

st.title("🌍✨ Mas-AI Multilingual Video Platform ✨🌍")

video_url = st.text_input("🔗 Paste YouTube URL here:", placeholder="https://www.youtube.com/...")

languages = {
    "🇺🇸 English": "en",
    "🇪🇸 Spanish": "es",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇨🇳 Chinese": "zh"
}

subtitle_choice = st.selectbox("📖 Subtitle Language", options=list(languages.keys()))
audio_choice = st.selectbox("🎧 Audio Language", options=list(languages.keys()))

def translate_text(text, lang_code):
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Translate this to {lang_code}: {text}"}]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']

def generate_audio(text, lang_code):
    audio = gTTS(text=text, lang=lang_code)
    audio.save("audio.mp3")

if st.button("🚀 Generate & Play 🚀"):
    with st.spinner("✨ Generating your multilingual video..."):
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(filename="video.mp4")

        translated_text = translate_text(yt.description, languages[subtitle_choice])

        generate_audio(translated_text, languages[audio_choice])

        video_clip = VideoFileClip("video.mp4")
        audio_clip = AudioFileClip("audio.mp3").set_duration(video_clip.duration)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")

        st.success("🎬 Here is your AI-enhanced video:")
        st.video("final_video.mp4")

        os.remove("video.mp4")
        os.remove("audio.mp3")
        os.remove("final_video.mp4")
