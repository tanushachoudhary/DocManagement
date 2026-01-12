from sentence_transformers import SentenceTransformer
import numpy as np

# Re-loading model (if this is a separate file). 
# Note: In a real app, load the model only once in a configuration file.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --- In-Memory Storage ---
# We use Python lists to store data.
# Strengths: Simple, fast for small data (<1000 docs).
# Weaknesses: Data is lost when app restarts; slow for millions of docs.
document_embeddings = []  # Stores the vectors (math meaning)
document_ids = []         # Stores the unique ID (to link back to SQL)
document_texts = []       # Stores the raw text (for debugging/display)

def index_document(doc_id: str, text: str):
    """
    Processes a document and saves it to our in-memory list.
    """
    # 1. Convert text to vector
    embedding = model.encode(text)
    
    # 2. Append data to our lists (keeping indices synchronized)
    document_embeddings.append(embedding)
    document_ids.append(doc_id)
    document_texts.append(text)