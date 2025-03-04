import streamlit as st
import pythoncom
import win32com.client
from deep_translator import GoogleTranslator
from lan import languages
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

st.set_page_config(page_title="Language Translator", layout="wide")

st.markdown("<h1 style='text-align: center;'>Language Translator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])


def translate_text():
    text_input = st.session_state.input_text
    target_lang = st.session_state.target_lang

    if text_input:
        try:
            translated_text = GoogleTranslator(source="auto", target=languages[target_lang]).translate(text_input)
            st.session_state.translated_text = translated_text

            if target_lang in ["Hindi", "Marathi", "Sanskrit","Nepali"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.DEVANAGARI, sanscript.HK).lower()
            elif target_lang in ["Bengali", "Assamese"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.BENGALI, sanscript.HK).lower()
            elif target_lang in ["Telugu"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.TELUGU, sanscript.HK).lower()
            elif target_lang in ["Tamil"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.TAMIL, sanscript.HK).lower()
            elif target_lang in ["Gujarati"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.GUJARATI, sanscript.HK).lower()
            elif target_lang in ["Malayalam"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.MALAYALAM, sanscript.HK).lower()
            elif target_lang in ["Kannada"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.KANNADA, sanscript.HK).lower()
            elif target_lang in ["Odia (Oriya)"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.ORIYA, sanscript.HK).lower()
            elif target_lang in ["Punjabi"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.GURMUKHI, sanscript.HK).lower()
            else:
                st.session_state.romanized_text = translated_text
        except Exception as e:
            st.warning("❌ Translation failed. Please try again.")


def speak_text():
    text = st.session_state.get("romanized_text", "")
    if text:
        try:
            pythoncom.CoInitialize()
            s = win32com.client.Dispatch("SAPI.SpVoice")
            s.Speak(text)
        except Exception as e:
            st.warning("❌ Failed to generate speech.")
    else:
        st.warning("❌ No text to read.")


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

    if st.button("🔊 Speak Translation"):
        speak_text()

st.markdown("<style>textarea {font-size: 20px;}</style>", unsafe_allow_html=True)























