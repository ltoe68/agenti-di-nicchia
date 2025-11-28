import pandas as pd
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

def load_gl_map(csv_path="gl_codes.csv"):
    try:
        return pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame(columns=["vendor_name", "gl_code", "gl_description"])

def predict_gl_code(description, gl_map_df):
    """Uses LLM to predict GL code based on description and available codes."""
    llm = ChatOpenAI(temperature=0, model_name=os.getenv("LLM_MODEL", "gpt-3.5-turbo"))
    
    # Create a context string of available codes
    codes_context = gl_map_df[['gl_code', 'gl_description']].drop_duplicates().to_string(index=False)
    
    prompt = PromptTemplate(
        template="""
        You are an Expert Accountant. Assign the correct General Ledger (GL) Code to an expense based on its description.
        Choose ONLY from the available codes below.
        
        AVAILABLE GL CODES:
        {codes_context}
        
        EXPENSE DESCRIPTION:
        {description}
        
        OUTPUT FORMAT:
        Return ONLY the GL Code (e.g., 6010). If unsure, pick the closest match.
        """,
        input_variables=["codes_context", "description"]
    )
    
    chain = prompt | llm
    return chain.invoke({
        "codes_context": codes_context,
        "description": description
    }).content.strip()

def assign_gl_code(invoice_data):
    """
    Assigns GL code:
    1. Exact match on Vendor Name.
    2. Fallback to LLM prediction on Description.
    """
    df = load_gl_map()
    vendor = invoice_data.get("vendor", "").lower()
    
    # 1. Exact/Fuzzy Match (Simple 'contains' for MVP)
    # Check if any known vendor string is contained in the extracted vendor name
    match = df[df['vendor_name'].str.lower().apply(lambda x: x in vendor or vendor in x)]
    
    if not match.empty:
        row = match.iloc[0]
        return {
            "gl_code": row['gl_code'],
            "gl_description": row['gl_description'],
            "method": "Vendor Lookup (Exact Match)"
        }
    
    # 2. Fallback: AI Prediction
    description = invoice_data.get("description", "")
    predicted_code = predict_gl_code(description, df)
    
    # Look up description for the predicted code
    desc_row = df[df['gl_code'].astype(str) == predicted_code]
    predicted_desc = desc_row.iloc[0]['gl_description'] if not desc_row.empty else "Unknown"
    
    return {
        "gl_code": predicted_code,
        "gl_description": predicted_desc,
        "method": "AI Prediction (Fallback)"
    }
