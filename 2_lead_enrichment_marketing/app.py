import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from main import process_dataframe

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Lead Enrichment Agent", page_icon="🚀")

st.title("🚀 Lead Enrichment Agent")
st.markdown("Upload a CSV with a `Company Name` column, and I'll find their details.")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    provider = os.getenv("LLM_PROVIDER", "openai")
    st.info(f"**Provider:** {provider}")
    
    st.markdown("### Instructions")
    st.markdown("1. Prepare a CSV file.")
    st.markdown("2. Ensure it has a column named `Company Name`.")
    st.markdown("3. Upload below.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "Company Name" not in df.columns:
            st.error("Error: CSV must contain a 'Company Name' column.")
        else:
            st.write("Preview of uploaded data:")
            st.dataframe(df.head())
            
            if st.button("Start Enrichment"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(current, total, message):
                    progress = int((current / total) * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"{message} ({current}/{total})")
                
                with st.spinner("Enriching leads... This may take a while."):
                    enriched_df = process_dataframe(df, progress_callback=update_progress)
                
                st.success("Enrichment Complete!")
                st.dataframe(enriched_df)
                
                csv = enriched_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Enriched CSV",
                    data=csv,
                    file_name="enriched_leads.csv",
                    mime="text/csv",
                )
                
    except Exception as e:
        st.error(f"Error reading file: {e}")
