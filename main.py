from document_loader import load_documents, chunk_documents
from vector_store import VectorStore
from rag_pipeline import RAGPipeline
from evaluator import Evaluator
from prompt_manager import IMPROVEMENTS

def setup_pipeline():
    print("\n" + "="*60)
    print("RAG SYSTEM - POLICY Q&A")
    print("="*60)
    
    print("\nLoading documents...")
    documents = load_documents()
    
    if not documents:
        print("No documents found. Exiting.")
        return None, None
    
    print("\nChunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    print("\nSetting up vector store...")
    vector_store = VectorStore()
    
    if not vector_store.collection_exists():
        vector_store.add_documents(chunks)
    else:
        print("Using existing vector store")
    
    return RAGPipeline(prompt_version="v2"), Evaluator()

def run_demo():
    pipeline, evaluator = setup_pipeline()
    
    if not pipeline:
        return
    
    print("\n" + "="*60)
    print("DEMO QUERIES")
    print("="*60)
    
    demo_questions = [
        "What is the refund policy?",
        "How long do I have to return an item?",
        "What is the shipping cost?",
        "Do you offer same-day delivery to space?"
    ]
    
    for question in demo_questions:
        print(f"\nQuestion: {question}")
        result = pipeline.answer_question(question)
        print(f"Answer: {result['answer'][:200]}...")
        print(f"Retrieved documents: {result['retrieved_documents']}")

def run_evaluation():
    pipeline, evaluator = setup_pipeline()
    
    if not pipeline:
        return
    
    print("\n" + "="*60)
    print("EVALUATION")
    print("="*60)
    
    test_questions = [
        {
            "question": "What is your refund policy and how long do I have?",
            "type": "answerable",
            "notes": "Should be covered in refund policy"
        },
        {
            "question": "Can I cancel my order after it shipped?",
            "type": "partial",
            "notes": "Partially covered in cancellation policy"
        },
        {
            "question": "Do you offer same-day delivery to all countries?",
            "type": "unanswerable",
            "notes": "Not covered in documents"
        },
        {
            "question": "How much does standard shipping cost?",
            "type": "answerable",
            "notes": "Should be in shipping policy"
        },
        {
            "question": "What items are not eligible for refund?",
            "type": "answerable",
            "notes": "Should be in refund policy"
        },
        {
            "question": "Is there a warranty on products?",
            "type": "unanswerable",
            "notes": "Not covered in provided policies"
        },
        {
            "question": "Can I get a refund if item arrived damaged?",
            "type": "answerable",
            "notes": "Special case in refund policy"
        },
        {
            "question": "How do I cancel a recurring subscription?",
            "type": "unanswerable",
            "notes": "Not covered in policies"
        }
    ]
    
    for i, test_q in enumerate(test_questions, 1):
        print(f"\n[{i}/8] {test_q['question']}")
        result = pipeline.answer_question(test_q['question'])
        evaluator.evaluate_answer(
            test_q['question'],
            result['answer'],
            test_q['type'],
            test_q['notes']
        )
    
    print("\n" + "="*60)
    print("PROMPT IMPROVEMENTS (V1 -> V2)")
    print("="*60)
    
    for key, improvement in IMPROVEMENTS.items():
        print(f"{key}: {improvement}")
    
    print("\n" + "="*60)
    print("SAVING RESULTS")
    print("="*60)
    
    evaluator.save_results("eval_results.json")

if __name__ == "__main__":
    print("\nChoose operation:")
    print("1. Run demo queries")
    print("2. Run evaluation")
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        run_demo()
    elif choice == "2":
        run_evaluation()
    elif choice == "3":
        run_demo()
        run_evaluation()
    else:
        print("Invalid choice")
