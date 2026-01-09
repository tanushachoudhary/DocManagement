from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---- In-memory vector store (TESTABLE) ----
vectors: List[np.ndarray] = []
document_ids: List[int] = []
documents_text: List[str] = []


def reset_store():
    vectors.clear()
    document_ids.clear()
    documents_text.clear()


def index_document(document_id: int, text: str):
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    if document_id in document_ids:
        raise ValueError("Document already indexed")

    embedding = model.encode(text)
    vectors.append(embedding)
    document_ids.append(document_id)
    documents_text.append(text)


def search(query: str, top_k: int = 5):
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    if not vectors:
        return []

    query_embedding = model.encode(query)

    scores = [
        float(np.dot(query_embedding, vec) /
              (np.linalg.norm(query_embedding) * np.linalg.norm(vec)))
        for vec in vectors
    ]

    ranked = sorted(
        zip(document_ids, documents_text, scores),
        key=lambda x: x[2],
        reverse=True
    )

    return [
        {
            "document_id": doc_id,
            "score": score,
            "text": text
        }
        for doc_id, text, score in ranked[:top_k]
    ]
