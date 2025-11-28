import os
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = os.getenv("LLM_MODEL", "gpt-4") # Default to GPT-4 for complex contracts
    
    if provider == "openai":
        return ChatOpenAI(temperature=0, model_name=model_name)
    elif provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(model=model_name, base_url=base_url)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file object."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def analyze_contract(text):
    """Analyzes the contract text using LLM."""
    llm = get_llm()
    
    # Define output structure
    response_schemas = [
        ResponseSchema(name="parties", description="List of parties involved (Landlord, Tenant)."),
        ResponseSchema(name="property_address", description="The full address of the property."),
        ResponseSchema(name="lease_term", description="Start date, End date, and Duration."),
        ResponseSchema(name="rent_amount", description="Monthly rent amount and currency."),
        ResponseSchema(name="security_deposit", description="Security deposit amount."),
        ResponseSchema(name="red_flags", description="List of risky or unusual clauses (e.g., Tenant pays structural repairs, No break clause).")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
        You are an expert Real Estate Lawyer. Review the following Lease Agreement and extract key details.
        Pay special attention to "Red Flags" - clauses that are unfair or risky for the Tenant.
        
        CONTRACT TEXT:
        {text}
        
        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions": format_instructions}
    )

    # Handle token limits by truncating if necessary (naive approach for MVP)
    # GPT-4 Turbo has 128k context, so usually fine. GPT-3.5 might struggle with long leases.
    if len(text) > 50000:
        text = text[:50000] + "... [TRUNCATED]"

    chain = prompt | llm | output_parser
    
    try:
        return chain.invoke({"text": text})
    except Exception as e:
        return {
            "parties": "Error",
            "property_address": "Error",
            "lease_term": "Error",
            "rent_amount": "Error",
            "security_deposit": "Error",
            "red_flags": f"Analysis failed: {str(e)}"
        }
