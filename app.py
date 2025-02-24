import streamlit as st
from pytube import YouTube
import openai
import os
from moviepy.editor import *
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Page setup
st.set_page_config(page_title="Mas-AI Multilingual Video Platform", layout="centered")
st.title("🚀 Mas-AI Multilingual Video Platform")

# User inputs
video_url = st.text_input("🔗 Paste YouTube video URL here:")
subtitle_lang = st.selectbox("📖 Choose Subtitle Language", ["English", "Spanish", "French", "German", "Chinese"])
audio_lang = st.selectbox("🎧 Choose Audio Language", ["English", "Spanish", "French", "German", "Chinese"])

# Main functionality
if st.button("✨ AI Transform & Play ✨"):
    if video_url:
        with st.spinner("Downloading and processing..."):
            # Download video clearly
            yt = YouTube(video_url)
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video_path = video_stream.download()

            st.success("Video downloaded successfully!")

            # AI-driven multilingual subtitle (example translation)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Translate the following text into {subtitle_lang}: {yt.description}"
                }]
            )
            translated_subtitle = response.choices[0].message.content

            # Display the AI-generated subtitle
            st.markdown(f"### 🎬 Video Description ({subtitle_lang})")
            st.write(translated_subtitle)

            # Display video player clearly
            st.video(video_path)

            # Clean up local video file clearly
            os.remove(video_path)
    else:
        st.error("⚠️ Please enter a valid YouTube URL.")
