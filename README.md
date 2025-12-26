#RAG System - Policy Q&A Assistant

A Retrieval-Augmented Generation (RAG) system that answers policy questions using Google Gemini API. The system loads policy documents, creates embeddings, performs semantic retrieval, and generates grounded answers with minimal hallucination.

## Project Structure

```
project/
├── config.py                 Configuration and API keys
├── document_loader.py        Load and chunk documents
├── vector_store.py           ChromaDB vector database interface
├── prompt_manager.py         Prompt templates (V1 and V2)
├── rag_pipeline.py           RAG orchestration and generation
├── evaluator.py              Evaluation framework
├── main.py                   Entry point
├── .env                      Environment variables (API key)
├── requirements.txt          Python dependencies
├── data/
│   └── policies/
│       ├── refund_policy.md
│       ├── shipping_policy.md
│       └── cancellation_policy.md
└── vector_db/               ChromaDB persistent storage
```

## Setup

### Requirements
- Python 3.8+
- Google Gemini API key (free from https://aistudio.google.com/app/apikeys)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create .env file:
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

Replace `your-api-key-here` with your actual Gemini API key from Google AI Studio.

3. Run the system:
```bash
python main.py
```

The system will prompt you to choose between:
- Run demo queries
- Run evaluation
- Both

## Architecture

### Document Loading and Chunking
- Reads Markdown policy documents from `data/policies/`
- Uses recursive character text splitter with 500-token chunks and 50-token overlap
- Chunk size balances context relevance with retrieval efficiency
- 50-token overlap ensures semantic continuity across chunks

### Vector Storage
- Uses ChromaDB for persistent vector database
- Google Generative AI embeddings for semantic representation
- Collection stored in `vector_db/` directory
- Supports incremental updates and efficient similarity search

### Retrieval
- Semantic search using cosine similarity
- Retrieves top-3 most relevant documents by default
- Returns document content and source metadata

### Generation
- Uses Google Gemini API (gemini-pro model)
- Two prompt versions for comparison
- Formats retrieved context into prompt template
- Returns structured answers grounded in documents

## Prompts

### Prompt V1 (Initial)
Conversational style with basic instructions. Less structured, easier to hallucinate.

### Prompt V2 (Improved)
Task-oriented approach with explicit guardrails:
1. Ground your answer in documents
2. Declare uncertainty explicitly
3. No invented dates or percentages
4. Structured output format
5. Clear context boundaries
6. Source citation requirement

### Improvements Made (V1 to V2)

1. **Explicit grounding instruction** - Added "Ground your answer" to prevent hallucination
2. **Declare uncertainty** - Encourages honest "I don't know" responses instead of guesses
3. **Structured output format** - Requires bullet points and clear formatting
4. **No invented numbers** - Specific examples of what not to invent
5. **Clear context boundaries** - Added ---CONTEXT_START/END--- markers
6. **Task description format** - More reliable than conversational instructions
7. **Source citation** - Requires citing which document information came from

Reasoning: V1 was too conversational; models often ignore conversational instructions. V2 uses imperative language and explicit task framing which is more reliable for LLM behavior.

## Evaluation Framework

### Metrics

1. **Accuracy** - Does the answer match the documents?
2. **Hallucination** - Does the answer contain invented information?
3. **Clarity** - Is the answer well-structured and understandable?
4. **Completeness** - Does the answer address all parts of the question?

### Scoring System

- Good - Positive response
- Partial - Minor issues or limitations
- Error - Significant problems

### Test Set (8 Questions)

Question types:
- **Answerable** - Fully covered in documents
- **Partial** - Partially mentioned
- **Unanswerable** - Not in documents

Examples:
1. What is your refund policy and how long do I have? (answerable)
2. Can I cancel my order after it shipped? (partial)
3. Do you offer same-day delivery to all countries? (unanswerable)
4. How much does standard shipping cost? (answerable)
5. What items are not eligible for refund? (answerable)
6. Is there a warranty on products? (unanswerable)
7. Can I get a refund if item arrived damaged? (answerable)
8. How do I cancel a recurring subscription? (unanswerable)

## Edge Cases Handled

### No Relevant Documents
System returns "No relevant documents found. I cannot answer this question."

### Out-of-Domain Questions
Off-topic questions are handled gracefully with honest uncertainty responses from Prompt V2

### Empty or Malformed Documents
Document loader validates files and skips problematic content

### API Failures
Error messages are returned to user with clear indication that generation failed

## Usage Examples

### Run Demo Queries
```bash
python main.py
# Choose option 1
```

Runs 4 sample questions to demonstrate the system works:
- Basic policy question
- Specific policy detail
- Shipping information
- Impossible question (same-day delivery to space)

### Run Evaluation
```bash
python main.py
# Choose option 2
```

Runs 8-question evaluation set and saves results to `eval_results.json`

### Both
```bash
python main.py
# Choose option 3
```

Runs demo followed by evaluation.

## Configuration

Key settings in `config.py`:

```python
CHUNK_SIZE = 500           # Characters per chunk
CHUNK_OVERLAP = 50         # Character overlap between chunks
RETRIEVAL_TOP_K = 3        # Number of documents to retrieve
MODEL_NAME = "gemini-pro"  # Gemini model to use
```

Adjust these based on document size and requirements.

## Trade-offs and Design Decisions

### Chunk Size (500 tokens)
- Trade-off: Larger chunks preserve more context but reduce retrieval precision
- 500 tokens is balance between relevance and efficiency
- Could increase to 750-1000 for larger policy documents

### Retrieval Top-K (3 documents)
- Trade-off: More documents increase context but consume more tokens
- 3 is sufficient for policy Q&A task
- Could increase to 5 for more comprehensive answers

### Prompt Structure
- Task-oriented Prompt V2 chosen over conversational V1
- Requires explicit citation of sources
- Trade-off: More structured output vs complete answer freedom

### Vector Store (ChromaDB)
- Persistent storage allows incremental updates
- Trade-off: Disk space vs avoiding re-embedding

## Future Improvements

### High Priority
1. Automatic prompt optimization loop instead of manual V1->V2
2. Query rewriting to improve retrieval
3. Re-ranking retrieved documents by relevance

### Medium Priority
1. Caching layer for repeated questions
2. Conversation memory for multi-turn Q&A
3. Fine-tuned embeddings for domain-specific retrieval

### Advanced
1. Active learning to identify hard questions
2. Automatic evaluation using other LLMs
3. Multi-stage retrieval with coarse-to-fine filtering
4. Structured extraction of key information

## Limitations

1. Retrieves based on lexical/semantic similarity, not logical relationships
2. No access to real-time data or external information
3. Answer quality depends entirely on document quality
4. Prompts optimized for English only
5. No conversation history or context carrying

## Evaluation Results

Results saved to `eval_results.json` after running evaluation.

Format:
```json
{
  "total_questions": 8,
  "results": [
    {
      "question": "...",
      "answer": "...",
      "question_type": "answerable",
      "accuracy": "good",
      "hallucination": "good",
      "clarity": "good",
      "completeness": "good",
      "notes": "..."
    }
  ]
}
```

## Troubleshooting

### API Key Invalid
- Verify key is correct in .env file
- Check key is active at https://aistudio.google.com/app/apikeys
- Ensure Generative AI API is enabled in Google Cloud project

### No Documents Found
- Verify data/policies/ folder exists
- Ensure markdown files are in correct location
- Check file encoding is UTF-8

### Vector Store Issues
- Delete vector_db/ folder to force re-embedding
- Ensure chromadb is properly installed

### Import Errors
- Run: pip install -r requirements.txt
- Verify Python version 3.8+

## License

This project is provided as-is for educational purposes.

## Support

For questions or issues, refer to the setup instructions above or review the architecture section for system design details.
