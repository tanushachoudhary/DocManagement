from fastapi import APIRouter
from sentence_transformers import SentenceTransformer
import numpy as np

# Import the in-memory data lists (our "Database")
from app.services.vector_store import (
    document_embeddings,
    document_ids,
    document_texts,
)

router = APIRouter()

# Initialize the AI Model
# This converts text into numbers. We use the exact same model used during indexing.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@router.post("/search")
def semantic_search(query: str, top_k: int = 3):
    """
    Performs semantic search using Cosine Similarity.
    1. Converts query to vector.
    2. Compares query vector against ALL document vectors.
    3. Returns the top K closest matches.
    """
    
    # Safety Check: If our "database" is empty, return nothing.
    if not document_embeddings:
        return {"results": []}

    # 1. Convert User Query to Vector
    # "Where is the refund?" -> [-0.01, 0.05, 0.12, ...]
    query_embedding = model.encode(query)

    # 2. Calculate Cosine Similarity (The Core Math)
    # This formula calculates the angle between the query vector and every document vector.
    # High score (1.0) = Very similar meaning.
    # Low score (0.0) = Unrelated.
    similarities = np.dot(
        document_embeddings, 
        query_embedding
    ) / (
        np.linalg.norm(document_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # 3. Sort Results
    # np.argsort returns the INDICES of the sorted elements (low to high).
    # [-top_k:] takes the last K items (the highest scores).
    # [::-1] reverses the list so the best match is first.
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    # 4. Format Output
    results = []
    for idx in top_indices:
        results.append({
            "document_id": document_ids[idx],       # Get the original ID
            "score": float(similarities[idx]),      # The similarity score (e.g., 0.85)
            "text": document_texts[idx][:500]       # Return preview of text
        })

    return {"results": results}