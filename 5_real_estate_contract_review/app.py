import streamlit as st
import os
from dotenv import load_dotenv
from analyzer import extract_text_from_pdf, analyze_contract

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Lease Review AI", page_icon="🏠")

st.title("🏠 Lease Review AI")
st.markdown("Upload a Lease Agreement (PDF) to extract key dates and red flags.")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    provider = os.getenv("LLM_PROVIDER", "openai")
    st.info(f"**Provider:** {provider}")
    st.warning("Note: GPT-4 is recommended for accurate legal analysis.")

uploaded_file = st.file_uploader("Upload Lease Agreement (.pdf)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)
    
    if text:
        st.success(f"Extracted {len(text)} characters.")
        with st.expander("View Raw Text"):
            st.text(text[:2000] + "...")
            
        if st.button("Analyze Contract"):
            with st.spinner("Analyzing clauses... This may take a minute."):
                analysis = analyze_contract(text)
            
            st.divider()
            
            # Display Results
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📍 Property")
                st.info(analysis.get("property_address", "N/A"))
                
                st.subheader("👥 Parties")
                st.write(analysis.get("parties", "N/A"))
                
            with c2:
                st.subheader("💰 Financials")
                st.metric("Rent", analysis.get("rent_amount", "N/A"))
                st.metric("Deposit", analysis.get("security_deposit", "N/A"))
                
            st.subheader("📅 Term")
            st.write(analysis.get("lease_term", "N/A"))
            
            st.divider()
            
            st.subheader("🚩 Red Flags & Risks")
            red_flags = analysis.get("red_flags", [])
            if isinstance(red_flags, list) and len(red_flags) > 0:
                for flag in red_flags:
                    st.error(f"• {flag}")
            elif isinstance(red_flags, str):
                 st.error(red_flags)
            else:
                st.success("No major red flags detected (or analysis returned empty).")
                
    else:
        st.error("Could not extract text. The PDF might be an image scan (OCR required).")
