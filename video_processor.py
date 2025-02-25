import os
import openai
import cv2
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip
from google.cloud import translate_v2 as translate, texttospeech
from pytube import YouTube

translate_client = translate.Client()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Download YouTube Video
def download_youtube_video(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, "video.mp4")
    stream.download(filename=video_path)
    return video_path, yt

# Translate Text
def translate_text(text, target_language):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']

# Generate AI Voice
def generate_ai_voice(text, target_language):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=target_language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content

# Sync Lips with Wav2Lip AI
def sync_lips(video_path, translated_audio_path, output_path):
    command = f"python wav2lip.py --checkpoint_path models/wav2lip.pth --face {video_path} --audio {translated_audio_path} --outfile {output_path}"
    os.system(command)

# Process Video Translation
def process_video_translation(video_path, target_language):
    audio_clip = AudioFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".mp3")
    audio_clip.write_audiofile(audio_path, codec='mp3')

    translated_text = translate_text("This is a test translation", target_language)
    translated_audio = generate_ai_voice(translated_text, target_language)

    translated_audio_path = video_path.replace(".mp4", "_translated.mp3")
    with open(translated_audio_path, "wb") as out:
        out.write(translated_audio)

    output_video_path = video_path.replace(".mp4", "_translated.mp4")
    sync_lips(video_path, translated_audio_path, output_video_path)

    return output_video_path
