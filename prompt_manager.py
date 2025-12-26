PROMPT_V1 = """You are a helpful assistant for answering questions about company policies.

Based on the documents provided, answer the user's question clearly and concisely.

If the answer is not in the documents, say "I don't know" rather than guessing.

Question: {question}

Documents:
{context}

Answer:"""

PROMPT_V2 = """Task: Answer policy questions based only on provided documents.

Context documents:
---CONTEXT_START---
{context}
---CONTEXT_END---

Instructions:
1. Ground your answer in the documents above
2. If information is not in documents, explicitly state "Not covered in provided documents"
3. Do not invent dates, percentages, or specific numbers
4. Use structured format with bullet points for clarity
5. Cite which document the information came from

Question: {question}

Answer:"""

IMPROVEMENTS = {
    "improvement_1": "Added explicit 'Ground your answer' instruction",
    "improvement_2": "Added 'Declare uncertainty' to encourage honest 'I don't know'",
    "improvement_3": "Added structured output format requirement",
    "improvement_4": "Emphasized 'No invented numbers' with specific examples",
    "improvement_5": "Clear context boundaries (---CONTEXT_START/END---)",
    "improvement_6": "Reformatted as task description vs conversational tone",
    "improvement_7": "Required citation of source documents"
}
