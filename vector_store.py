import chromadb
from langchain.embeddings import GooglePalmEmbeddings
from config import VECTOR_DB_PATH, GEMINI_API_KEY

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        self.embeddings = GooglePalmEmbeddings(google_api_key=GEMINI_API_KEY)
        self.collection_name = "policies"
    
    def collection_exists(self):
        try:
            self.client.get_collection(self.collection_name)
            return True
        except:
            return False
    
    def add_documents(self, chunks):
        if self.collection_exists():
            self.client.delete_collection(self.collection_name)
        
        collection = self.client.get_or_create_collection(self.collection_name)
        
        for i, chunk in enumerate(chunks):
            embedding = self.embeddings.embed_query(chunk["content"])
            collection.add(
                ids=[f"chunk_{i}"],
                embeddings=[embedding],
                documents=[chunk["content"]],
                metadatas=[{"source": chunk["source"]}]
            )
        
        print(f"Added {len(chunks)} chunks to vector store")
    
    def retrieve(self, query, top_k=3):
        collection = self.client.get_collection(self.collection_name)
        
        query_embedding = self.embeddings.embed_query(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        retrieved = []
        if results and results["documents"]:
            for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
                retrieved.append({
                    "content": doc,
                    "source": metadata.get("source", "unknown")
                })
        
        return retrieved
