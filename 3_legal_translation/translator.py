import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

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

def translate_text(text, target_language="Italian", glossary=None):
    llm = get_llm()
    
    glossary_text = ""
    if glossary:
        glossary_text = "\nMANDATORY TERMINOLOGY (You MUST use these translations):\n"
        for src, tgt in glossary.items():
            glossary_text += f"- {src} -> {tgt}\n"
    
    # System prompt specialized for legal documents
    system_template = """You are an expert legal translator with 20 years of experience in international law.
    Your task is to translate the following legal document section into {target_language}.
    
    GUIDELINES:
    1. Maintain extreme precision with legal terminology.
    2. Preserve the original formatting, numbering (1.1, (a), etc.), and structure.
    3. Do not summarize. Translate every sentence.
    4. If a term is ambiguous, prefer the standard legal equivalent in the target jurisdiction.
    5. Maintain a formal and professional tone.
    {glossary_text}
    """
    
    human_template = "{text}"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template)
    ])
    
    chain = prompt | llm
    
    # Split text if it's too long (simple splitting for MVP)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    translated_chunks = []
    
    print(f"Translating {len(chunks)} chunks...")
    
    for i, chunk in enumerate(chunks):
        print(f"  - Chunk {i+1}/{len(chunks)}")
        try:
            response = chain.invoke({
                "target_language": target_language, 
                "text": chunk,
                "glossary_text": glossary_text
            })
            # Handle different response types from LangChain (String or Message)
            content = response.content if hasattr(response, 'content') else str(response)
            translated_chunks.append(content)
        except Exception as e:
            print(f"Error translating chunk {i}: {e}")
            translated_chunks.append(f"[TRANSLATION ERROR: {e}]")
            
    return "\n\n".join(translated_chunks)
