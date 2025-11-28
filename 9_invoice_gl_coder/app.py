import streamlit as st
import os
from dotenv import load_dotenv
from extractor import extract_text_from_pdf, parse_invoice
from coder import assign_gl_code

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Invoice GL Coder", page_icon="🧾")

st.title("🧾 Invoice GL Coder")
st.markdown("Upload an invoice to automatically assign the General Ledger code.")

# Sidebar: GL Codes
with st.sidebar:
    st.header("GL Codes Mapping")
    try:
        import pandas as pd
        df = pd.read_csv("gl_codes.csv")
        st.dataframe(df, hide_index=True)
    except:
        st.error("gl_codes.csv not found.")

uploaded_file = st.file_uploader("Upload Invoice (PDF)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting data..."):
        text = extract_text_from_pdf(uploaded_file)
        invoice_data = parse_invoice(text)
    
    if "error" in invoice_data:
        st.error(f"Error parsing invoice: {invoice_data['error']}")
    else:
        st.subheader("1. Extracted Data")
        c1, c2, c3 = st.columns(3)
        c1.metric("Vendor", invoice_data.get("vendor"))
        c2.metric("Date", invoice_data.get("date"))
        c3.metric("Total", invoice_data.get("total_amount"))
        st.caption(f"Description: {invoice_data.get('description')}")
        
        st.divider()
        
        with st.spinner("Assigning GL Code..."):
            coding_result = assign_gl_code(invoice_data)
            
        st.subheader("2. GL Assignment")
        
        col_code, col_desc, col_method = st.columns(3)
        
        col_code.metric("GL Code", coding_result["gl_code"])
        col_desc.metric("Account", coding_result["gl_description"])
        
        if "AI" in coding_result["method"]:
            col_method.warning(f"Method: {coding_result['method']}")
        else:
            col_method.success(f"Method: {coding_result['method']}")
            
        st.divider()
        st.json(invoice_data | coding_result)
