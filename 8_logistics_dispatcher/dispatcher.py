import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from db_lookup import lookup_shipment

def get_llm():
    model_name = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    return ChatOpenAI(temperature=0, model_name=model_name)

def extract_order_id(email_text):
    """Extracts the Order ID from the email text."""
    llm = get_llm()
    
    response_schemas = [
        ResponseSchema(name="order_id", description="The tracking number or order ID found in the email. If none, return null.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    
    prompt = PromptTemplate(
        template="""
        Extract the Order ID or Tracking Number from the following customer email.
        If there are multiple numbers, pick the one that looks most like an order ID (e.g., 5 digits).
        
        EMAIL:
        {email}
        
        {format_instructions}
        """,
        input_variables=["email"],
        partial_variables={"format_instructions": format_instructions}
    )
    
    chain = prompt | llm | output_parser
    
    try:
        result = chain.invoke({"email": email_text})
        return result.get("order_id")
    except Exception as e:
        print(f"Extraction error: {e}")
        return None

def draft_response(email_text, order_info):
    """Drafts a polite response based on the order info."""
    llm = get_llm()
    
    if order_info and "error" not in order_info:
        status_context = f"""
        Order ID: {order_info.get('order_id')}
        Status: {order_info.get('status')}
        Location: {order_info.get('location')}
        Expected Delivery: {order_info.get('delivery_date')}
        """
        instruction = "The order was found. Inform the customer about the status politely."
    else:
        status_context = "Order ID not found in our database."
        instruction = "Apologize and ask the customer to double-check the ID or provide more details."
        
    prompt = PromptTemplate(
        template="""
        You are a Customer Service Agent for a Logistics Company.
        Draft a polite and professional email response to the customer.
        
        CUSTOMER EMAIL:
        {email}
        
        SYSTEM INFORMATION:
        {status_context}
        
        INSTRUCTION:
        {instruction}
        
        DRAFT RESPONSE:
        """,
        input_variables=["email", "status_context", "instruction"]
    )
    
    chain = prompt | llm
    return chain.invoke({
        "email": email_text,
        "status_context": status_context,
        "instruction": instruction
    }).content

def process_email(email_text):
    """Orchestrates the flow: Extract -> Lookup -> Draft."""
    order_id = extract_order_id(email_text)
    
    if order_id:
        order_info = lookup_shipment(order_id)
    else:
        order_info = None
        
    draft = draft_response(email_text, order_info)
    
    return {
        "extracted_id": order_id,
        "db_result": order_info,
        "draft_response": draft
    }
