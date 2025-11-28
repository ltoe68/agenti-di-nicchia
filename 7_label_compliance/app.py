import streamlit as st
import os
from dotenv import load_dotenv
from vision_analyzer import analyze_label

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Label Compliance AI", page_icon="🏷️")

st.title("🏷️ Label Compliance AI")
st.markdown("Upload a food label image to check for regulatory issues (EU/FDA).")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("LLM_MODEL", "gpt-4o")
    st.info(f"**Model:** {model}")
    st.warning("Requires a Vision-capable model (GPT-4o, GPT-4-Turbo).")

uploaded_file = st.file_uploader("Upload Label Image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Label", use_column_width=True)
    
    if st.button("Analyze Compliance"):
        with st.spinner("Analyzing label... (This uses GPT-4 Vision)"):
            # Reset file pointer before reading in analyzer
            uploaded_file.seek(0)
            report = analyze_label(uploaded_file)
        
        st.subheader("Compliance Report")
        st.markdown(report)
        
        st.download_button(
            label="Download Report",
            data=report,
            file_name="compliance_report.md",
            mime="text/markdown"
        )
