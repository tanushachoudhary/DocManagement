from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# 1. LOAD THE AI MODEL
# We use "all-MiniLM-L6-v2", a small but fast model designed for semantic search.
# It converts any text into a fixed-size list of 384 numbers.
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. IN-MEMORY STORAGE (The "Database")
# In a real production app, you would replace these lists with 
# a vector database like FAISS, ChromaDB, or Pinecone.
vectors: List[np.ndarray] = []     # Stores the mathematical meaning (384 numbers)
document_ids: List[int] = []       # Stores the ID to link back to MySQL
documents_text: List[str] = []     # Stores the raw text for display


def reset_store():
    """Clears all data. Useful for running clean tests."""
    vectors.clear()
    document_ids.clear()
    documents_text.clear()


def index_document(document_id: int, text: str):
    """
    Converts a document's text into a vector and saves it.
    """
    # Validation
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    if document_id in document_ids:
        raise ValueError(f"Document ID {document_id} already indexed")

    # CORE LOGIC: Convert text -> Vector (Embedding)
    embedding = model.encode(text)
    
    # Save to memory
    vectors.append(embedding)
    document_ids.append(document_id)
    documents_text.append(text)


def search(query: str, top_k: int = 5):
    """
    Finds the most similar documents to the query.
    Uses Cosine Similarity to compare vectors.
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    if not vectors:
        return []

    # 1. Convert the USER QUERY into a vector
    query_embedding = model.encode(query)

    # 2. CALCULATE SIMILARITY SCORES
    # We compare the query vector against EVERY stored document vector.
    # Formula: Cosine Similarity = (A . B) / (||A|| * ||B||)
    scores = [
        float(np.dot(query_embedding, vec) /
              (np.linalg.norm(query_embedding) * np.linalg.norm(vec)))
        for vec in vectors
    ]

    # 3. RANK RESULTS
    # Combine IDs, Text, and Scores into a single list
    results = zip(document_ids, documents_text, scores)
    
    # Sort by score (Highest match first)
    ranked = sorted(
        results,
        key=lambda x: x[2], # Sort by score (index 2)
        reverse=True        # Descending order
    )

    # 4. FORMAT OUTPUT
    return [
        {
            "document_id": doc_id,
            "score": score,
            "text": text
        }
        for doc_id, text, score in ranked[:top_k] # Return only top K results
    ]