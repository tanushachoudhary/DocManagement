from fastapi import APIRouter
from sentence_transformers import SentenceTransformer
import numpy as np

from app.services.vector_store import (
    document_embeddings,
    document_ids,
    document_texts,
)

router = APIRouter()

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@router.post("/search")
def semantic_search(query: str, top_k: int = 3):
    if not document_embeddings:
        return {"results": []}

    query_embedding = model.encode(query)

    similarities = np.dot(
        document_embeddings,
        query_embedding
    ) / (
        np.linalg.norm(document_embeddings, axis=1)
        * np.linalg.norm(query_embedding)
    )

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "document_id": document_ids[idx],
            "score": float(similarities[idx]),
            "text": document_texts[idx][:500]
        })

    return {"results": results}
