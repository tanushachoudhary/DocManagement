import faiss
import numpy as np
import pickle
import os
from app.services.embeddings import generate_embedding

# File paths for persistence
INDEX_FILE = "vector_index.faiss"
STORE_FILE = "doc_store.pkl"

DIMENSION = 384  # all-MiniLM-L6-v2
index = faiss.IndexFlatIP(DIMENSION)  # cosine similarity
documents = []  # stores chunk text + metadata

def add_chunks(chunks: list[str], metadata: list[dict]):
    global index, documents
    
    if not chunks:
        return

    # 1. Generate Vectors
    vectors = np.array(
        [generate_embedding(chunk) for chunk in chunks]
    ).astype("float32")

    # 2. Add to FAISS Index
    index.add(vectors)

    # 3. Add to Memory Store
    for i, chunk in enumerate(chunks):
        documents.append({
            "content": chunk,
            "metadata": metadata[i]
        })
    
    # 4. Save to Disk immediately
    save_index()

def similarity_search(query: str, k=5, score_threshold=0.4):
    # Reload logic could go here, but usually we load on startup (see main.py)
    if index.ntotal == 0:
        return []

    query_vec = generate_embedding(query).astype("float32").reshape(1, -1)
    scores, indices = index.search(query_vec, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        # faiss returns -1 if not found
        if idx != -1 and score >= score_threshold:
            # Ensure we don't go out of bounds if documents weren't synced
            if idx < len(documents):
                results.append(documents[idx])

    return results

def get_chunks_by_doc_id(doc_id): # remove type hint for flexible input
    results = []
    
    # Debug print: See what's actually in memory
    print(f"DEBUG: Total documents in memory: {len(documents)}")
    
    for doc in documents:
        stored_id = doc["metadata"].get("document_id")
        
        # Compare as strings to be safe
        if str(stored_id) == str(doc_id):
            results.append(doc)
            
    return results

# --- Persistence Methods ---

def save_index():
    """Saves the FAISS index and the documents list to disk."""
    # Save FAISS index
    faiss.write_index(index, INDEX_FILE)
    
    # Save Documents list (Text + Metadata)
    with open(STORE_FILE, "wb") as f:
        pickle.dump(documents, f)
    print("Index and Documents saved to disk.")

def load_index():
    """Loads the FAISS index and documents list from disk."""
    global index, documents
    
    if os.path.exists(INDEX_FILE) and os.path.exists(STORE_FILE):
        # Load FAISS
        index = faiss.read_index(INDEX_FILE)
        
        # Load Documents
        with open(STORE_FILE, "rb") as f:
            documents = pickle.load(f)
            
        print(f"Loaded {index.ntotal} vectors and {len(documents)} chunks from disk.")
    else:
        print("No existing index found. Starting fresh.")