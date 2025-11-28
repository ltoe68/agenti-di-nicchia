import os
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

def get_llm():
    model_name = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
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

def parse_invoice(text):
    """Extracts structured data from invoice text."""
    llm = get_llm()
    
    response_schemas = [
        ResponseSchema(name="vendor", description="The name of the vendor/supplier."),
        ResponseSchema(name="date", description="The invoice date (YYYY-MM-DD)."),
        ResponseSchema(name="total_amount", description="The total amount due."),
        ResponseSchema(name="description", description="A brief summary of the line items or services provided.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    
    prompt = PromptTemplate(
        template="""
        Extract key information from the following invoice text.
        
        INVOICE TEXT:
        {text}
        
        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions": format_instructions}
    )
    
    chain = prompt | llm | output_parser
    
    try:
        return chain.invoke({"text": text[:4000]}) # Truncate to avoid token limits
    except Exception as e:
        return {"error": str(e)}
