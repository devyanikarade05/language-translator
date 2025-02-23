import streamlit as st
from deep_translator import GoogleTranslator
from lan import languages
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import epitran
import pyttsx3  # Offline TTS
import threading  # For non-blocking TTS

st.set_page_config(page_title="Language Translator", layout="wide")

st.markdown("<h1 style='text-align: center;'>Language Translator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# Function to handle text-to-speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to translate text
def translate_text():
    text_input = st.session_state.input_text
    target_lang = st.session_state.target_lang

    if text_input:
        try:
            translated_text = GoogleTranslator(source="auto", target=languages[target_lang]).translate(text_input)
            st.session_state.translated_text = translated_text

            # Transliteration for Indic languages
            if target_lang in ["Hindi", "Marathi", "Sanskrit"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.DEVANAGARI, sanscript.ITRANS).lower()
            elif target_lang in ["Bengali", "Assamese"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.BENGALI, sanscript.ITRANS).lower()
            elif target_lang in ["Telugu"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.TELUGU, sanscript.ITRANS).lower()
            elif target_lang in ["Tamil"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.TAMIL, sanscript.ITRANS).lower()
            elif target_lang in ["Gujarati"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.GUJARATI, sanscript.ITRANS).lower()
            elif target_lang in ["Malayalam"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.MALAYALAM, sanscript.ITRANS).lower()
            elif target_lang in ["Kannada"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.KANNADA, sanscript.ITRANS).lower()
            elif target_lang in ["Odia (Oriya)"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.ORIYA, sanscript.ITRANS).lower()
            elif target_lang in ["Punjabi"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.GURMUKHI, sanscript.ITRANS).lower()
            else:
                try:
                    epi = epitran.Epitran(languages[target_lang])
                    st.session_state.romanized_text = epi.transliterate(translated_text).lower()
                except:
                    st.session_state.romanized_text = translated_text

        except Exception as e:
            st.warning("❌ Translation failed. Please try again.")

# Left Column - Input
with col1:
    st.subheader("🔡 Enter Text")
    text_input = st.text_area("Type here...", key="input_text", height=350)

    if st.button("Translate"):
        translate_text()

# Right Column - Output
with col2:
    st.subheader("Translation")
    st.selectbox("Translate to", list(languages.keys()), key="target_lang", on_change=translate_text)

    translated_output = st.text_area("Translated Text", st.session_state.get("translated_text", ""), height=150)
    romanized_output = st.text_area("Romanized Text", st.session_state.get("romanized_text", ""), height=100)

    # 🔊 Speaker Button to Play Translated Text
    if st.session_state.get("translated_text", ""):
        if st.button("🔊 Play Translation"):
            threading.Thread(target=speak_text, args=(st.session_state["translated_text"],)).start()

st.markdown("<style>textarea {font-size: 18px;}</style>", unsafe_allow_html=True)











