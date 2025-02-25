import os
import requests
import streamlit as st
from emoji import emojize
import base64
from dotenv import load_dotenv
import os


load_dotenv()

# Load Google API Key from environment variables
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define available languages with flags
languages = {
    "en": "🇺🇸 English",
    "es": "🇪🇸 Spanish",
    "fr": "🇫🇷 French",
    "de": "🇩🇪 German",
    "zh": "🇨🇳 Chinese",
    "it": "🇮🇹 Italian",
    "ru": "🇷🇺 Russian",
    "ja": "🇯🇵 Japanese",
    "hi": "🇮🇳 Hindi",
    "ar": "🇸🇦 Arabic"
}

# Function to translate text
def translate_text(text, target_language):
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_language,
        "format": "text",
        "key": GOOGLE_TRANSLATE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["data"]["translations"][0]["translatedText"]
    return "Translation Error"

# Function for adding a custom mouse cursor effect (CSS + JavaScript)
def add_custom_styles():
    st.markdown(
        """
        <style>
            body {
                background: linear-gradient(to right, #1e3c72, #2a5298);
                color: white;
                font-family: 'Arial', sans-serif;
            }
            .stApp {
                background: linear-gradient(to right, #1e3c72, #2a5298);
            }
            .stTextInput input, .stTextArea textarea {
                border-radius: 15px;
                background: white;
                color: black;
            }
            .stButton>button {
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                border: none;
                color: white;
                padding: 10px 20px;
                font-size: 18px;
                border-radius: 20px;
                transition: all 0.3s ease-in-out;
            }
            .stButton>button:hover {
                transform: scale(1.1);
                background: linear-gradient(to right, #feb47b, #ff7e5f);
            }
            #fancy-cursor {
                position: fixed;
                width: 12px;
                height: 12px;
                background: radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(255,255,255,0.5) 50%);
                border-radius: 50%;
                pointer-events: none;
                transform: translate(-50%, -50%);
                z-index: 9999;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
            }
        </style>
        <script>
            document.addEventListener("mousemove", function(e) {
                var cursor = document.getElementById("fancy-cursor");
                cursor.style.top = e.clientY + "px";
                cursor.style.left = e.clientX + "px";
            });
        </script>
        <div id="fancy-cursor"></div>
        """,
        unsafe_allow_html=True
    )

# UI setup
def main():
    add_custom_styles()
    st.title("🌎 Mas-AI Multilingual Video Platform")
    
    # YouTube Video Input
    video_url = st.text_input("🔗 Paste YouTube video URL here:", "")
    
    # Language Selection with Flags
    target_lang = st.selectbox("📖 Subtitle Language", languages.keys(), format_func=lambda x: languages[x])
    
    # Translate Button
    if st.button("✨ Translate & Play ✨"):
        translated_text = translate_text("Hello, how are you?", target_lang)
        st.success(f"{languages[target_lang]} {translated_text}")
        
    # Fancy Footer
    st.markdown(
        """
        <div style="text-align:center; padding-top:20px;">
            <p>🚀 Powered by Mas-AI Consulting | Google Cloud Translation API</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
