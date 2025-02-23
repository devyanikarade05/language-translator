import streamlit as st
from deep_translator import GoogleTranslator
from lan import languages
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import epitran
from gtts import gTTS
import base64
import os

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

            if target_lang in ["Hindi", "Marathi", "Sanskrit"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.DEVANAGARI,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Bengali", "Assamese"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.BENGALI,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Telugu"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.TELUGU,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Tamil"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.TAMIL,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Gujarati"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.GUJARATI,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Malayalam"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.MALAYALAM,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Kannada"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.KANNADA,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Odia (Oriya)"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.ORIYA,
                                                                sanscript.ITRANS).lower()
            elif target_lang in ["Punjabi"]:
                st.session_state.romanized_text = transliterate(translated_text, sanscript.GURMUKHI,
                                                                sanscript.ITRANS).lower()

            else:
                try:
                    epi = epitran.Epitran(languages[target_lang])
                    st.session_state.romanized_text = epi.transliterate(translated_text).lower()
                except:
                    st.session_state.romanized_text = translated_text
        except Exception as e:
            st.warning("❌ Translation failed. Please try again.")


def speak_text():
    if st.session_state.get("translated_text", ""):
        try:
            tts = gTTS(text=st.session_state["translated_text"], lang=languages[st.session_state["target_lang"]])
            audio_file = "output.mp3"
            tts.save(audio_file)

            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
                st.session_state.audio_base64 = base64.b64encode(audio_bytes).decode()

            os.remove(audio_file)
        except Exception as e:
            st.error("❌ Error in text-to-speech. Please try again.")


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

    if st.session_state.get("translated_text", ""):
        if st.button("🔊 Play Translation"):
            speak_text()

    if st.session_state.get("audio_base64", ""):
        st.markdown(
            f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{st.session_state.audio_base64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True
        )

st.markdown("<style>textarea {font-size: 18px;}</style>", unsafe_allow_html=True)












