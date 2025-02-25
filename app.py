import streamlit as st
import google.auth
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from pytube import YouTube
import tempfile
import os
import openai
import base64
import torch
import librosa
import numpy as np
import ffmpeg
import soundfile as sf
import json
from moviepy.editor import *
from Wav2Lip.models import Wav2Lip

# Load API keys from environment variables
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Set up Google Cloud Translation API
translate_client = translate.Client()

# Set up OpenAI API for voice cloning
openai.api_key = OPENAI_API_KEY

# Fetch all available languages from Google Translate
LANGUAGES = translate_client.get_languages()
LANGUAGE_DICT = {lang['language']: lang['name'] for lang in LANGUAGES}

# Function to translate text
def translate_text(text, target_language):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

# Function to generate AI voice using OpenAI TTS
def generate_voice(text, target_language):
    response = openai.Audio.create(
        engine="tts-1",
        text=text,
        voice="alloy",
        language=target_language
    )
    return response['data']

# Function to download YouTube video
def download_youtube_video(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, "video.mp4")
    stream.download(filename=video_path)
    return video_path, yt

# Function to process audio translation
def process_audio_translation(video_path, target_language):
    audio_clip = AudioFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    audio_clip.write_audiofile(audio_path, codec='pcm_s16le')
    
    translated_text = translate_text("This is a sample translation", target_language)
    translated_audio = generate_voice(translated_text, target_language)
    translated_audio_path = video_path.replace(".mp4", "_translated.wav")
    
    with open(translated_audio_path, "wb") as out:
        out.write(translated_audio)
    
    return translated_audio_path

# Function to synchronize lips using Wav2Lip
def sync_lip_movement(video_path, translated_audio_path):
    output_path = video_path.replace(".mp4", "_synced.mp4")
    os.system(f"python Wav2Lip/inference.py --checkpoint_path Wav2Lip/checkpoints/wav2lip.pth --face {video_path} --audio {translated_audio_path} --outfile {output_path}")
    return output_path

# Streamlit UI
def main():
    st.set_page_config(page_title="AI Multilingual Video Translator", layout="wide")
    st.title("🌎 AI Multilingual Video Translator")
    st.markdown("**Real-time AI-powered voice and subtitle translation for videos!**")
    
    video_url = st.text_input("🎥 Paste YouTube Video URL:")
    target_language = st.selectbox("🌍 Select Target Language:", options=LANGUAGE_DICT.keys(), format_func=lambda x: LANGUAGE_DICT[x])
    
    if st.button("🚀 Translate Video"):
        with st.spinner("Processing video..."):
            video_path, yt = download_youtube_video(video_url)
            translated_audio_path = process_audio_translation(video_path, target_language)
            final_video_path = sync_lip_movement(video_path, translated_audio_path)
            
            st.success("Translation Complete!")
            st.video(final_video_path)

if __name__ == "__main__":
    main()
