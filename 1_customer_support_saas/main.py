import os
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

def get_llm_and_embeddings():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    print(f"Configuring agent with Provider: {provider}, Model: {model_name}")

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found for provider 'openai'")
        embeddings = OpenAIEmbeddings()
        llm = ChatOpenAI(temperature=0, model_name=model_name)
    elif provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        embeddings = OllamaEmbeddings(model=model_name, base_url=base_url)
        llm = ChatOllama(model=model_name, base_url=base_url)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    
    return llm, embeddings

def create_rag_chain():
    """Initializes and returns the RAG chain."""
    try:
        llm, embeddings = get_llm_and_embeddings()
    except Exception as e:
        print(f"Configuration Error: {e}")
        return None

    # 1. Load Knowledge Base
    try:
        loader = TextLoader("./knowledge_base/docs.md")
        documents = loader.load()
        print(f"Loaded {len(documents)} document(s) from knowledge base.")
    except Exception as e:
        print(f"Error loading documents: {e}")
        return None

    # 2. Create Embeddings and Vector Store
    try:
        vectorstore = FAISS.from_documents(documents, embeddings)
        print("Vector store created successfully.")
    except Exception as e:
        print(f"Error creating vector store: {e}")
        print("Tip: If using Ollama, make sure 'ollama serve' is running and the model is pulled.")
        return None

    # 3. Setup Retrieval Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    return qa_chain

def main():
    print("Initializing Customer Support Agent...")
    
    qa_chain = create_rag_chain()
    if not qa_chain:
        print("Failed to initialize agent.")
        return

    print("\nAgent is ready! (Type 'exit' to quit)")
    print("-" * 30)

    # 4. Interaction Loop
    while True:
        query = input("\nUser: ")
        if query.lower() in ['exit', 'quit', 'q']:
            break
        
        try:
            response = qa_chain.invoke(query)
            print(f"Agent: {response['result']}")
        except Exception as e:
            print(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
