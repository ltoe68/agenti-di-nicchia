import os
import pandas as pd
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

def get_llm():
    model_name = os.getenv("LLM_MODEL", "gpt-4") # GPT-4 recommended for messy tables
    return ChatOpenAI(temperature=0, model_name=model_name)

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return ""

def extract_bom(text):
    """Extracts Bill of Materials from text."""
    llm = get_llm()
    
    # Define schema for a list of items
    response_schemas = [
        ResponseSchema(name="items", description="List of items. Each item should have 'name', 'description', 'quantity', 'unit'.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    
    prompt = PromptTemplate(
        template="""
        You are a Quantity Surveyor. Extract a Bill of Materials (BOM) from the construction specification text below.
        Identify all materials, works, or items that require a cost estimate.
        
        If a quantity is specified, extract it. If not, leave it as "1" or "To Estimate".
        
        SPECIFICATION TEXT:
        {text}
        
        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions": format_instructions}
    )
    
    # Chunking strategy needed for long docs, but for MVP we truncate or assume short specs
    # Using a larger context window model (GPT-4-Turbo) is best here.
    chain = prompt | llm | output_parser
    
    try:
        # Truncate to ~50k chars for safety if using standard context
        result = chain.invoke({"text": text[:50000]})
        return result.get("items", [])
    except Exception as e:
        print(f"Extraction error: {e}")
        return []

def items_to_df(items):
    if not items:
        return pd.DataFrame(columns=["Item Name", "Description", "Quantity", "Unit", "Unit Price", "Total"])
    
    df = pd.DataFrame(items)
    # Add empty columns for the contractor to fill
    df["Unit Price"] = 0.0
    df["Total"] = 0.0
    return df
