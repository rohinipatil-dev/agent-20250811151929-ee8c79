import os
import streamlit as st
from openai import OpenAI


LANGUAGE_OPTIONS = {
    "Hindi (हिंदी)": "Hindi",
    "Tamil (தமிழ்)": "Tamil",
    "Telugu (తెలుగు)": "Telugu",
    "Kannada (ಕನ್ನಡ)": "Kannada",
    "Malayalam (മലയാളം)": "Malayalam",
    "Bengali (বাংলা)": "Bengali",
    "Marathi (मराठी)": "Marathi",
    "Gujarati (ગુજરાતી)": "Gujarati",
    "Punjabi (ਪੰਜਾਬੀ)": "Punjabi",
}


def get_client() -> OpenAI:
    return OpenAI()


def translate_text(client: OpenAI, english_text: str, target_language: str) -> str:
    if not english_text.strip():
        return ""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": (
                        f"Translate the following English text into {target_language}.\n"
                        "Return only the translation text with no additional commentary, no labels, and no quotes.\n"
                        "Preserve meaning, tone, and natural phrasing. Keep formatting and line breaks where reasonable.\n\n"
                        f"Text:\n{english_text.strip()}"
                    ),
                },
            ],
            temperature=0.2,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        raise RuntimeError(str(e)) from e


def build_ui():
    st.set_page_config(page_title="English → Indian Languages Translator", page_icon="🌐", layout="centered")
    st.title("English → Indian Languages Translator")
    st.caption("Translate English text into Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, or Punjabi.")

    with st.expander("How to use", expanded=False):
        st.markdown(
            "- Select a target language.\n"
            "- Enter English text to translate.\n"
            "- Click Translate to get the result below.\n"
        )

    lang_display = st.selectbox("Target language", options=list(LANGUAGE_OPTIONS.keys()))
    target_language = LANGUAGE_OPTIONS[lang_display]

    english_text = st.text_area(
        "Enter English text",
        height=180,
        placeholder="Type or paste your English text here...",
    )

    col1, col2 = st.columns([1, 1])
    translate_clicked = col1.button("Translate", type="primary")
    clear_clicked = col2.button("Clear")

    if clear_clicked:
        st.experimental_rerun()

    return target_language, english_text, translate_clicked


def main():
    target_language, english_text, translate_clicked = build_ui()

    if translate_clicked:
        if not english_text.strip():
            st.warning("Please enter some English text to translate.")
            return

        if not os.environ.get("OPENAI_API_KEY"):
            st.info("Set your OpenAI API key in the OPENAI_API_KEY environment variable to run translations.")
        with st.spinner("Translating..."):
            try:
                client = get_client()
                translation = translate_text(client, english_text, target_language)
                if translation:
                    st.subheader("Translated Text")
                    st.text_area(
                        label="",
                        value=translation,
                        height=200,
                        key="translated_text_display",
                    )
                else:
                    st.info("No translation produced. Please try again.")
            except Exception as e:
                st.error(f"Translation failed: {e}")


if __name__ == "__main__":
    main()