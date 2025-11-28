import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    if provider == "openai":
        return ChatOpenAI(temperature=0, model_name=model_name)
    elif provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(model=model_name, base_url=base_url)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

def enrich_company_data(company_name, website_text):
    if not website_text:
        return {
            "description": "N/A",
            "industry": "N/A",
            "target_audience": "N/A",
            "pricing_model": "N/A"
        }

    llm = get_llm()
    
    # Define output structure
    response_schemas = [
        ResponseSchema(name="description", description="A one-sentence pitch of what the company does."),
        ResponseSchema(name="industry", description="The primary industry of the company."),
        ResponseSchema(name="target_audience", description="Who is their main customer? (B2B/B2C, specific roles)."),
        ResponseSchema(name="pricing_model", description="Any mention of pricing (Freemium, Subscription, Enterprise, or 'Not Visible').")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
        You are a business analyst. Analyze the following text scraped from a company's website and extract key information.
        
        Company Name: {company_name}
        Website Content:
        {website_text}
        
        {format_instructions}
        """,
        input_variables=["company_name", "website_text"],
        partial_variables={"format_instructions": format_instructions}
    )

    chain = prompt | llm | output_parser
    
    try:
        return chain.invoke({"company_name": company_name, "website_text": website_text})
    except Exception as e:
        print(f"Error enriching {company_name}: {e}")
        return {
            "description": "Error",
            "industry": "Error",
            "target_audience": "Error",
            "pricing_model": "Error"
        }
