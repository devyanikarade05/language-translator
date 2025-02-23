import streamlit as st
from deep_translator import GoogleTranslator
from lan import languages
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import epitran
from TTS.api import TTS

# Initialize Coqui TTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

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

            # Generate audio using Coqui TTS
            audio_file = "output.wav"
            tts.tts_to_file(text=translated_text, file_path=audio_file)
            st.session_state.audio_file = audio_file

        except Exception as e:
            st.warning("❌ Translation failed. Please try again.")

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

    # Add a button to play the audio
    if st.session_state.get("audio_file"):
        st.audio(st.session_state.audio_file, format='audio/wav')
        if st.button("Play Audio"):
            st.audio(st.session_state.audio_file, format='audio/wav', start_time=0)

st.markdown("<style>textarea {font-size: 18px;}</style>", unsafe_allow_html=True)












