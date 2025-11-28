import streamlit as st
import os
from dotenv import load_dotenv
from dispatcher import process_email

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Logistics Dispatcher AI", page_icon="🚚")

st.title("🚚 Logistics Dispatcher AI")
st.markdown("Paste a customer email to auto-draft a response based on shipment status.")

# Sidebar with Mock Data View
with st.sidebar:
    st.header("📦 Mock Database")
    st.info("This agent looks up data in `shipments.csv`.")
    try:
        import pandas as pd
        df = pd.read_csv("shipments.csv")
        st.dataframe(df, hide_index=True)
    except Exception:
        st.error("shipments.csv not found.")

email_input = st.text_area("Customer Email", height=150, placeholder="Hi, where is my order #12345?")

if st.button("Draft Response"):
    if email_input:
        with st.spinner("Processing..."):
            result = process_email(email_input)
        
        # Display Extraction Results
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔍 Extraction")
            if result["extracted_id"]:
                st.success(f"Order ID: {result['extracted_id']}")
            else:
                st.warning("No Order ID found.")
                
        with c2:
            st.subheader("🗄️ DB Lookup")
            if result["db_result"]:
                st.json(result["db_result"])
            else:
                st.error("Not found in DB.")
        
        st.divider()
        
        st.subheader("✉️ Draft Response")
        st.text_area("Edit before sending:", value=result["draft_response"], height=300)
        
    else:
        st.warning("Please paste an email first.")
