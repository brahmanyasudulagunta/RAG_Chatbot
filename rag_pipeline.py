import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Use absolute paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "data" / "pdfs"
DB_DIR = BASE_DIR / "data" / "chroma_db"

def ingest_pdfs():
    print(f"Ingesting PDFs from {PDF_DIR}...")
    
    if not PDF_DIR.exists():
        print(f"Directory {PDF_DIR} does not exist.")
        return None

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = []

    try:
        pdf_files = list(PDF_DIR.glob("*.pdf"))
        if not pdf_files:
            print("No PDF files found.")
            return None

        for file_path in pdf_files:
            try:
                print(f"Processing {file_path.name}...")
                loader = PyPDFLoader(str(file_path))
                docs = loader.load_and_split(text_splitter)
                documents.extend(docs)
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
        
        if documents:
            vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory=str(DB_DIR))
            print(f"Successfully ingested {len(documents)} chunks from {len(pdf_files)} files!")
            return vectordb
        else:
            print("No documents were successfully processed.")
            return None

    except Exception as e:
        print(f"Error during ingestion process: {e}")
        return None


def get_relevant_docs(query):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        if not DB_DIR.exists():
             print("Vector DB not found. Please run ingestion first.")
             return []
             
        vectordb = Chroma(persist_directory=str(DB_DIR), embedding_function=embeddings)
        results = vectordb.similarity_search(query, k=4)
        return results
    except Exception as e:
        print(f"Error retrieval documents: {e}")
        return []

if __name__ == "__main__":
    ingest_pdfs()
