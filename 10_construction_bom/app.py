import streamlit as st
import os
from dotenv import load_dotenv
from estimator import extract_text_from_pdf, extract_bom, items_to_df

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Construction BOM Estimator", page_icon="🏗️")

st.title("🏗️ Construction BOM Estimator")
st.markdown("Upload a Technical Specification (Capitolato) PDF to extract the Bill of Materials.")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    model = os.getenv("LLM_MODEL", "gpt-4")
    st.info(f"**Model:** {model}")
    st.warning("Complex tables require GPT-4 or better.")

uploaded_file = st.file_uploader("Upload Spec Sheet (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Reading PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.success(f"Read {len(text)} characters.")
        
    if st.button("Extract BOM"):
        with st.spinner("Analyzing specifications... (This may take a minute)"):
            items = extract_bom(text)
            df = items_to_df(items)
            
        st.subheader("📋 Bill of Materials")
        st.dataframe(df, use_container_width=True)
        
        # CSV Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV for Excel",
            data=csv,
            file_name="bom_estimate.csv",
            mime="text/csv",
        )
