from fastapi import FastAPI
from pytube import YouTube

app = FastAPI()

@app.get("/video-info")
def get_video_info(url: str):
    yt = YouTube(url)
    return {
        "title": yt.title,
        "duration": yt.length,
        "views": yt.views,
        "description": yt.description,
    }
