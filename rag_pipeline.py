import google.generativeai as genai
from prompt_manager import PROMPT_V1, PROMPT_V2
from config import GEMINI_API_KEY, MODEL_NAME, RETRIEVAL_TOP_K
from vector_store import VectorStore

genai.configure(api_key=GEMINI_API_KEY)

class RAGPipeline:
    def __init__(self, prompt_version="v2"):
        self.vector_store = VectorStore()
        self.model = genai.GenerativeModel(MODEL_NAME)
        self.prompt_version = prompt_version
        self.prompt_template = PROMPT_V2 if prompt_version == "v2" else PROMPT_V1
    
    def retrieve_context(self, query):
        results = self.vector_store.retrieve(query, top_k=RETRIEVAL_TOP_K)
        context = "\n\n".join([r["content"] for r in results])
        return context, results
    
    def generate_answer(self, question, context):
        if not context.strip():
            return "No relevant documents found. I cannot answer this question."
        
        prompt = self.prompt_template.format(question=question, context=context)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def answer_question(self, question):
        context, retrieved_docs = self.retrieve_context(question)
        answer = self.generate_answer(question, context)
        
        return {
            "question": question,
            "answer": answer,
            "retrieved_documents": len(retrieved_docs),
            "prompt_version": self.prompt_version
        }
