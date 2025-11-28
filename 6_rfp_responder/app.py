import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from ingest import ingest_documents
from generator import generate_answer

# Load environment variables
load_dotenv()

st.set_page_config(page_title="RFP Responder AI", page_icon="📝", layout="wide")

st.title("📝 RFP Responder AI")
st.markdown("Automate your RFP responses using your past winning proposals.")

# Sidebar for Knowledge Base
with st.sidebar:
    st.header("1. Knowledge Base")
    st.info("Upload past proposals (PDF, DOCX, TXT) to train the agent.")
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, type=["pdf", "docx", "txt", "md"])
    
    if st.button("Ingest Documents"):
        if uploaded_files:
            with st.spinner("Indexing documents..."):
                # Save to temp dir to pass paths to ingest function
                temp_files = []
                for uploaded_file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                        tmp.write(uploaded_file.getvalue())
                        temp_files.append(tmp.name)
                
                result = ingest_documents(temp_files)
                st.success(result)
                
                # Cleanup temp files
                for f in temp_files:
                    os.remove(f)
        else:
            st.warning("Please upload at least one file.")

# Main Area for New RFP
st.header("2. Answer New RFP")

# Option A: Paste Question
question = st.text_area("Paste a question from the RFP:", height=100)

if st.button("Draft Answer"):
    if question:
        with st.spinner("Searching Knowledge Base and drafting answer..."):
            answer = generate_answer(question)
        st.subheader("Draft Answer")
        st.write(answer)
        st.button("Copy to Clipboard") # Streamlit doesn't support direct copy yet, but button implies intent
    else:
        st.warning("Please enter a question.")

st.divider()
st.markdown("### Future Features")
st.markdown("- Upload full RFP PDF and auto-extract all questions.")
st.markdown("- Export to Word.")
