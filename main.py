import streamlit as st
import requests
import os
from deep_translator import GoogleTranslator
from lan import languages
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import epitran

st.set_page_config(page_title="Language Translator", layout="wide")

st.markdown("<h1 style='text-align: center;'>Language Translator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# Secure API Key Handling
MURF_API_KEY = os.getenv("MURF_API_KEY", "YOUR_API_KEY_HERE")  # Replace with your actual API key
MURF_API_URL = "https://api.murf.ai/v1/speech/generate"

def translate_text():
    text_input = st.session_state.input_text
    target_lang = st.session_state.target_lang

    if text_input:
        try:
            translated_text = GoogleTranslator(source="auto", target=languages[target_lang]).translate(text_input)
            st.session_state.translated_text = translated_text

            script_mapping = {
                "Hindi": sanscript.DEVANAGARI,
                "Marathi": sanscript.DEVANAGARI,
                "Sanskrit": sanscript.DEVANAGARI,
                "Bengali": sanscript.BENGALI,
                "Assamese": sanscript.BENGALI,
                "Telugu": sanscript.TELUGU,
                "Tamil": sanscript.TAMIL,
                "Gujarati": sanscript.GUJARATI,
                "Malayalam": sanscript.MALAYALAM,
                "Kannada": sanscript.KANNADA,
                "Odia (Oriya)": sanscript.ORIYA,
                "Punjabi": sanscript.GURMUKHI,
            }

            if target_lang in script_mapping:
                st.session_state.romanized_text = transliterate(
                    translated_text, script_mapping[target_lang], sanscript.ITRANS
                ).lower()
            else:
                try:
                    epi = epitran.Epitran(languages[target_lang])
                    st.session_state.romanized_text = epi.transliterate(translated_text).lower()
                except:
                    st.session_state.romanized_text = translated_text

            # Call Murf AI API for voice synthesis
            audio_url = generate_speech(translated_text, target_lang)
            if audio_url:
                st.session_state.audio_url = audio_url

        except Exception as e:
            st.warning(f"❌ Translation failed. Error: {e}")

def generate_speech(text, language):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api-key": MURF_API_KEY
    }

    payload = {
        "voiceId": "en-US-natalie",  # Adjust this based on language selection
        "style": "Promo",
        "text": text,
        "rate": 0,
        "pitch": 0,
        "sampleRate": 48000,
        "format": "MP3",
        "channelType": "MONO",
        "pronunciationDictionary": {},
        "encodeAsBase64": False,
        "variation": 1,
        "audioDuration": 0,
        "modelVersion": "GEN2",
        "multiNativeLocale": language
    }

    response = requests.post(MURF_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("audio_url")
    else:
        st.warning(f"❌ Voice synthesis failed. Response: {response.text}")
        return None

with col1:
    st.subheader("🔡 Enter Text")
    text_input = st.text_area("Type here...", key="input_text", height=350)

    if st.button("Translate"):
        translate_text()

with col2:
    st.subheader("Translation")
    st.selectbox("Translate to", list(languages.keys()), key="target_lang", on_change=translate_text)

    st.text_area("Translated Text", st.session_state.get("translated_text", ""), height=150)
    st.text_area("Romanized Text", st.session_state.get("romanized_text", ""), height=100)

    if "audio_url" in st.session_state:
        st.audio(st.session_state.audio_url, format="audio/mp3")

st.markdown("<style>textarea {font-size: 18px;}</style>", unsafe_allow_html=True)













