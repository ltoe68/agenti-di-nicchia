import streamlit as st
import pandas as pd
from matcher import reconcile_dataframes

st.set_page_config(page_title="Financial Reconciler", page_icon="💰", layout="wide")

st.title("💰 Financial Reconciler")
st.markdown("Compare two CSV/Excel files to find discrepancies (e.g., Stripe vs Bank).")

col1, col2 = st.columns(2)

with col1:
    st.subheader("File A (e.g. Source)")
    file_a = st.file_uploader("Upload File A", type=["csv", "xlsx"], key="a")

with col2:
    st.subheader("File B (e.g. Target)")
    file_b = st.file_uploader("Upload File B", type=["csv", "xlsx"], key="b")

if file_a and file_b:
    try:
        # Load files
        df_a = pd.read_csv(file_a) if file_a.name.endswith('.csv') else pd.read_excel(file_a)
        df_b = pd.read_csv(file_b) if file_b.name.endswith('.csv') else pd.read_excel(file_b)
        
        st.divider()
        st.subheader("Configuration")
        
        c1, c2 = st.columns(2)
        with c1:
            key_a = st.selectbox("Select ID Column for File A", df_a.columns)
        with c2:
            key_b = st.selectbox("Select ID Column for File B", df_b.columns)
            
        if st.button("Reconcile Files"):
            with st.spinner("Crunching numbers..."):
                results = reconcile_dataframes(df_a, df_b, key_a, key_b)
            
            summary = results["summary"]
            
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Matches", summary["matches"])
            m2.metric(f"Missing in File B", summary["missing_in_b"], delta_color="inverse")
            m3.metric(f"Missing in File A", summary["missing_in_a"], delta_color="inverse")
            
            st.divider()
            
            tab1, tab2, tab3 = st.tabs(["✅ Matched", "❌ Missing in B (Unmatched A)", "❌ Missing in A (Unmatched B)"])
            
            with tab1:
                st.dataframe(results["matched"])
            
            with tab2:
                st.warning(f"These {summary['missing_in_b']} rows exist in File A but NOT in File B.")
                st.dataframe(results["unmatched_a"])
                
            with tab3:
                st.warning(f"These {summary['missing_in_a']} rows exist in File B but NOT in File A.")
                st.dataframe(results["unmatched_b"])
                
    except Exception as e:
        st.error(f"Error processing files: {e}")
