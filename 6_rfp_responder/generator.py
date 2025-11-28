import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from ingest import get_retriever

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

def generate_answer(question):
    """
    Generates an answer for a specific RFP question using the Knowledge Base.
    """
    retriever = get_retriever()
    if not retriever:
        return "Error: Knowledge Base not found. Please ingest documents first."
    
    llm = get_llm()
    
    prompt_template = """You are a Proposal Writer. Your job is to answer a question from a new RFP (Request for Proposal) based on our company's past winning proposals.
    
    Use the following pieces of context to answer the question at the end. 
    If you don't know the answer based on the context, say "I don't have enough information in the Knowledge Base to answer this." and suggest what info is missing.
    Do not make up facts.
    
    CONTEXT:
    {context}
    
    QUESTION:
    {question}
    
    ANSWER (Draft a professional response):
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    try:
        response = chain.invoke(question)
        return response['result']
    except Exception as e:
        return f"Error generating answer: {e}"
