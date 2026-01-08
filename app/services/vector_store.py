from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# In-memory storage
document_embeddings = []
document_ids = []
document_texts = []

def index_document(doc_id: str, text: str):
    embedding = model.encode(text)
    document_embeddings.append(embedding)
    document_ids.append(doc_id)
    document_texts.append(text)
