import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_PATH

def load_documents():
    documents = []
    data_dir = Path(DATA_PATH)
    
    if not data_dir.exists():
        print(f"Warning: {DATA_PATH} directory not found")
        return documents
    
    for file_path in data_dir.glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append({
                "content": content,
                "source": file_path.name
            })
            print(f"Loaded: {file_path.name}")
    
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    for doc in documents:
        texts = splitter.split_text(doc["content"])
        for text in texts:
            chunks.append({
                "content": text,
                "source": doc["source"]
            })
    
    return chunks
