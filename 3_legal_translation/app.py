import streamlit as st
import os
from dotenv import load_dotenv
from translator import translate_text

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Legal Translator AI", page_icon="⚖️")

st.title("⚖️ Legal Translator AI")
st.markdown("Professional translation for legal documents (Contracts, NDAs).")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    provider = os.getenv("LLM_PROVIDER", "openai")
    st.info(f"**Provider:** {provider}")
    
    target_lang = st.selectbox("Target Language", ["Italian", "English", "Spanish", "French", "German"])
    
    st.markdown("### Glossary (Optional)")
    glossary_file = st.file_uploader("Upload Glossary (.csv)", type=["csv"])
    glossary = {}
    if glossary_file:
        try:
            import pandas as pd
            df = pd.read_csv(glossary_file, header=None)
            # Assume col 0 is source, col 1 is target
            if len(df.columns) >= 2:
                glossary = dict(zip(df[0], df[1]))
                st.success(f"Loaded {len(glossary)} terms.")
            else:
                st.error("CSV must have at least 2 columns (Source, Target).")
        except Exception as e:
            st.error(f"Error reading glossary: {e}")

uploaded_file = st.file_uploader("Upload a document (.txt, .md)", type=["txt", "md"])

if uploaded_file is not None:
    # Read file
    stringio = uploaded_file.getvalue().decode("utf-8")
    
    st.subheader("Original Text Preview")
    st.text_area("Source", value=stringio[:1000] + ("..." if len(stringio) > 1000 else ""), height=200, disabled=True)
    
    if st.button("Translate Document"):
        with st.spinner("Translating... This requires precision and may take a moment."):
            translated_text = translate_text(stringio, target_language=target_lang, glossary=glossary)
        
        st.success("Translation Complete!")
        
        st.subheader("Translated Text")
        st.text_area("Result", value=translated_text, height=400)
        
        st.download_button(
            label="Download Translation",
            data=translated_text,
            file_name=f"translated_{uploaded_file.name}",
            mime="text/plain"
        )
