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

# Initialize session state
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "romanized_text" not in st.session_state:
    st.session_state.romanized_text = ""

# Function to handle text-to-speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to translate text
def translate_text():
    text_input = st.session_state.get("input_text", "").strip()
    target_lang = st.session_state.get("target_lang", "")

    if text_input and target_lang:
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
            st.warning(f"❌ Translation failed: {str(e)}")

# Left Column - Input
with col1:
    st.subheader("🔡 Enter Text")
    st.text_area("Type here...", key="input_text", height=350)

    if st.button("Translate"):
        translate_text()

# Right Column - Output
with col2:
    st.subheader("Translation")
    st.selectbox("Translate to", list(languages.keys()), key="target_lang")

    if st.button("🔄 Run Translation"):
        translate_text()

    st.text_area("Translated Text", st.session_state.get("translated_text", ""), height=150)
    st.text_area("Romanized Text", st.session_state.get("romanized_text", ""), height=100)

    # 🔊 Speaker Button to Play Translated Text
    if st.session_state.get("translated_text", ""):
        if st.button("🔊 Play Translation"):
            threading.Thread(target=speak_text, args=(st.session_state["translated_text"],)).start()

st.markdown("<style>textarea {font-size: 18px;}</style>", unsafe_allow_html=True)











