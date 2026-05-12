# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is a technique that grants LLMs access to specific, up-to-date information without the need for constant retraining. It works by retrieving relevant document chunks from a vector database and providing them as context to the model during the generation phase.

Key components of RAG:
1. **Retrieval**: Finding the most relevant documents based on user query embedding.
2. **Augmentation**: Combining the user query with the retrieved context.
3. **Generation**: The LLM producing an answer based on the augmented prompt.

Benefits of RAG:
- Reduces hallucinations by grounding answers in facts.
- Provides citations and transparency.
- Enables easy updates to the knowledge base.
