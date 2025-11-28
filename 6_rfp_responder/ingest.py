import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

DB_DIR = "./chroma_db"

def get_embeddings():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "openai":
        return OpenAIEmbeddings()
    elif provider == "ollama":
        return OllamaEmbeddings(model=os.getenv("LLM_MODEL", "llama2"))
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def ingest_documents(files):
    """
    Ingests a list of file paths (PDF, DOCX, TXT) into the vector database.
    """
    documents = []
    for file_path in files:
        try:
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            elif file_path.endswith(".txt") or file_path.endswith(".md"):
                loader = TextLoader(file_path)
            else:
                continue
            
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    if not documents:
        return "No documents loaded."

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    embeddings = get_embeddings()
    
    # Persist to disk
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    vectorstore.persist()
    
    return f"Successfully indexed {len(splits)} chunks from {len(files)} files."

def get_retriever():
    """Returns the retriever object from the existing vector DB."""
    embeddings = get_embeddings()
    if not os.path.exists(DB_DIR):
        return None
    
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})
