import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import epitran

st.set_page_config(page_title="Language Translator", layout="wide")

st.markdown("<h1 style='text-align: center;'>Language Translator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

languages = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Marathi": "mr",
    "Telugu": "te",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Urdu": "ur",
    "Kannada": "kn",
    "Odia (Oriya)": "or",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Assamese": "as",
    "Maithili": "mai",
    "Santali": "sat",
    "Kashmiri": "ks",
    "Konkani": "kok",
    "Sindhi": "sd",
    "Dogri": "doi",
    "Manipuri (Meitei)": "mni",
    "Bodo": "brx",
    "Nepali": "ne",
    "Sanskrit": "sa",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Maltese": "mt",
    "Maori": "mi",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tatar": "tt",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}

with col1:
    st.subheader("🔡 Enter Text")
    text_input = st.text_area("Type here...", height=400)

with col2:
    st.subheader("Translation")

    target_lang = st.selectbox("Translate to", list(languages.keys()))

    translated_text = ""
    romanized_text = ""

    if text_input:
        try:
            translated_text = GoogleTranslator(source="auto", target=languages[target_lang]).translate(text_input)

            if target_lang in ["Hindi", "Marathi", "Sanskrit"]:
                romanized_text = transliterate(translated_text, sanscript.DEVANAGARI, sanscript.ITRANS).lower()

            elif target_lang in ["Bengali", "Assamese"]:
                romanized_text = transliterate(translated_text, sanscript.BENGALI, sanscript.ITRANS).lower()

            elif target_lang in ["Telugu"]:
                romanized_text = transliterate(translated_text, sanscript.TELUGU, sanscript.ITRANS).lower()

            elif target_lang in ["Tamil"]:
                romanized_text = transliterate(translated_text, sanscript.TAMIL, sanscript.ITRANS).lower()

            elif target_lang in ["Gujarati"]:
                romanized_text = transliterate(translated_text, sanscript.GUJARATI, sanscript.ITRANS).lower()

            elif target_lang in ["Urdu", "Kashmiri"]:
                romanized_text = transliterate(translated_text, sanscript.URDU, sanscript.ITRANS).lower()

            elif target_lang in ["Malayalam"]:
                romanized_text = transliterate(translated_text, sanscript.MALAYALAM, sanscript.ITRANS).lower()

            elif target_lang in ["Kannada"]:
                romanized_text = transliterate(translated_text, sanscript.KANNADA, sanscript.ITRANS).lower()

            elif target_lang in ["Odia (Oriya)"]:
                romanized_text = transliterate(translated_text, sanscript.ORIYA, sanscript.ITRANS).lower()

            elif target_lang in ["Punjabi"]:
                romanized_text = transliterate(translated_text, sanscript.GURMUKHI, sanscript.ITRANS).lower()

            else:
                try:
                    epi = epitran.Epitran(languages[target_lang])
                    romanized_text = epi.transliterate(translated_text).lower()
                except:
                    romanized_text = translated_text


        except Exception as e:
            st.warning("❌ Translation failed. Please try again.")

    st.text_area("Translated Text", translated_text, height=150)
    st.text_area("Romanized Text", romanized_text, height=100)

st.markdown("<style>textarea {font-size: 18px;}</style>", unsafe_allow_html=True)





