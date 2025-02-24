import streamlit as st
from pytube import YouTube
from gtts import gTTS
import tempfile
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import requests
from io import BytesIO
import base64
import imageio
import imageio_ffmpeg as ffmpeg


imageio.plugins.ffmpeg.download()


st.set_page_config(
    page_title="✨ Mas-AI Multilingual Player ✨",
    layout="wide",
    page_icon="🚀"
)

# CSS for spectacular UI and sparkling cursor
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
    overflow-x: hidden;
}
@keyframes sparkle {
    0%, 100% { box-shadow: 0 0 8px white; }
    50% { box-shadow: 0 0 18px #4ADEDE, 0 0 28px #797EF6, 0 0 38px #1AA7EC; }
}
.sparkle-cursor {
    position: fixed;
    pointer-events: none;
    width: 15px;
    height: 15px;
    background: radial-gradient(circle, #4ADEDE, #797EF6, #1AA7EC);
    border-radius: 50%;
    animation: sparkle 1s infinite alternate;
    z-index: 9999;
}
.flag {
    height: 20px;
    width: 30px;
    border-radius: 4px;
    margin-right: 10px;
}
h1 {
    text-align: center;
    color: #FFF;
    font-family: 'Arial Black', sans-serif;
    margin-bottom: 30px;
}
button {
    background-color: #4ADEDE;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
}
</style>
<div class="sparkle-cursor" id="sparkle-cursor"></div>
<script>
document.addEventListener('mousemove', (e) => {
    const cursor = document.getElementById('sparkle-cursor');
    cursor.style.top = e.clientY + 'px';
    cursor.style.left = e.clientX + 'px';
});
</script>
""", unsafe_allow_html=True)

st.title("✨🚀 Mas-AI Multilingual Player 🚀✨")

video_url = st.text_input("🔗 Paste YouTube video URL:", "")

# Language selection with flags (popular languages)
languages = {
    'en': ('English', '🇺🇸'),
    'es': ('Spanish', '🇪🇸'),
    'fr': ('French', '🇫🇷'),
    'de': ('German', '🇩🇪'),
    'zh-CN': ('Chinese', '🇨🇳'),
    'ja': ('Japanese', '🇯🇵'),
    'ko': ('Korean', '🇰🇷'),
    'it': ('Italian', '🇮🇹'),
    'ru': ('Russian', '🇷🇺'),
    'fa': ('Persian', '🇮🇷'),
    # Add more as needed
}

lang_labels = [f"{flag} {name}" for code, (name, flag) in languages.items()]
selected_lang = st.selectbox("🎧 Select audio/subtitle language:", lang_labels)
lang_code = list(languages.keys())[lang_labels.index(selected_lang)]

if st.button("✨ Generate Multilingual Video ✨"):
    with st.spinner("Generating your multilingual AI video..."):
        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()

            # Download video
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            stream.download(output_path=os.path.dirname(temp_video.name), filename=os.path.basename(temp_video.name))

            # Generate translated audio
            tts = gTTS(text=yt.title, lang=lang_code)
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_audio.name)

            # Merge audio & video
            video_clip = VideoFileClip(temp_video.name)
            audio_clip = AudioFileClip(temp_audio.name)
            video_clip = video_clip.set_audio(audio_clip)
            final_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
            video_clip.write_videofile(final_video_path, codec='libx264')

            # Display video
            with open(final_video_path, "rb") as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)

            # Clean up temporary files
            os.unlink(temp_video.name)
            os.unlink(temp_audio.name)
            os.unlink(final_video_path)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Powered by Mas-AI Consulting 🚀")

