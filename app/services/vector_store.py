import faiss
import numpy as np
import pickle
import os
from app.services.embeddings import generate_embedding

# ==========================================
# CONFIGURATION & PATHS
# ==========================================
# We determine the Project Root to ensure files are saved in the correct place,
# regardless of where you run the command from (Docker vs Windows).
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AI_DATA_DIR = os.path.join(BASE_DIR, "ai_index")

# Ensure the folder exists
os.makedirs(AI_DATA_DIR, exist_ok=True)

# Define absolute paths for persistence
INDEX_FILE = os.path.join(AI_DATA_DIR, "vector_index.faiss")
STORE_FILE = os.path.join(AI_DATA_DIR, "doc_store.pkl")

# ==========================================
# FAISS INITIALIZATION
# ==========================================
# Dimension 384 corresponds to the 'all-MiniLM-L6-v2' model.
# If you change the model, you MUST update this dimension.
DIMENSION = 384  

# We use IndexFlatIP (Inner Product). 
# Since embeddings are usually normalized, Inner Product == Cosine Similarity.
# This is the standard index for semantic search.
index = faiss.IndexFlatIP(DIMENSION)  

# This list mirrors the FAISS index.
# index[0] corresponds to documents[0].
# FAISS stores vectors (math), this list stores content (text).
documents = [] 

def add_chunks(chunks: list[str], metadata: list[dict]):
    """
    Embeds text chunks and adds them to both the FAISS index and local memory.
    Automatically saves to disk after adding.
    """
    global index, documents
    
    if not chunks:
        return

    # 1. Generate Vectors
    # Convert list of vectors to a numpy array of type float32 (Required by FAISS)
    vectors = np.array(
        [generate_embedding(chunk) for chunk in chunks]
    ).astype("float32")

    # 2. Add to FAISS Index (The math part)
    index.add(vectors)

    # 3. Add to Memory Store (The text part)
    # We must append in the EXACT same order as the vectors were added
    # to maintain the index <-> document mapping.
    for i, chunk in enumerate(chunks):
        documents.append({
            "content": chunk,
            "metadata": metadata[i]
        })
    
    # 4. Persistence
    # Save immediately to prevent data loss if the server restarts
    save_index()

# Lower threshold from 0.4 to 0.1 or 0.2 to let these matches through
def similarity_search(query: str, k=5, score_threshold=0.1):
    """
    Performs a semantic search.
    1. Embeds the user query.
    2. Searches FAISS for the nearest vectors.
    3. Retrieves the actual text content from the 'documents' list.
    """
    # Safety check: If the brain is empty, don't try to search
    if index.ntotal == 0:
        return []

    # Prepare query vector (1, Dimension)
    query_vec = generate_embedding(query).astype("float32").reshape(1, -1)
    
    # Perform Search
    # scores = similarity score (higher is better for Cosine/IP)
    # indices = the ID (0, 1, 2...) of the matching document in our list
    scores, indices = index.search(query_vec, k)

    results = []
    # Loop through results (indices[0] because we only searched 1 query)
    for score, idx in zip(scores[0], indices[0]):
        
        # FAISS returns -1 if it couldn't find k neighbors (rare in Flat index)
        if idx != -1:
            # Filter by relevance threshold (e.g., ignore weak matches < 0.4)
            if score >= score_threshold:
                # Safety Bound Check: Ensure we have the text for this vector
                if idx < len(documents):
                    doc = documents[idx]
                    # Inject the score into the result for debugging/UI display
                    doc["score"] = float(score) 
                    results.append(doc)

    return results

def get_chunks_by_doc_id(doc_id): 
    """
    Retrieves all text chunks belonging to a specific uploaded file.
    Useful for debugging: "Did my file actually get chunked?"
    """
    results = []
    
    print(f"DEBUG: Searching memory. Total docs: {len(documents)}")
    
    for doc in documents:
        # Access nested metadata safely
        stored_id = doc.get("metadata", {}).get("document_id")
        
        # Compare as strings to avoid TypeErrors (UUID vs str)
        if str(stored_id) == str(doc_id):
            results.append(doc)
            
    return results

# ==========================================
# PERSISTENCE METHODS
# ==========================================

def save_index():
    """
    Saves the vector state (FAISS) and text state (Pickle) to disk.
    This allows the AI to 'remember' data after a restart.
    """
    try:
        # Save FAISS index
        faiss.write_index(index, INDEX_FILE)
        
        # Save Documents list
        with open(STORE_FILE, "wb") as f:
            pickle.dump(documents, f)
            
        print(f"Index saved to {AI_DATA_DIR}")
    except Exception as e:
        print(f"Failed to save index: {e}")

def load_index():
    """
    Loads the AI brain from disk on startup.
    Call this in your main.py startup event.
    """
    global index, documents
    
    if os.path.exists(INDEX_FILE) and os.path.exists(STORE_FILE):
        try:
            # Load FAISS
            index = faiss.read_index(INDEX_FILE)
            
            # Load Text Data
            with open(STORE_FILE, "rb") as f:
                documents = pickle.load(f)
                
            print(f"Loaded brain: {index.ntotal} vectors from {AI_DATA_DIR}")
        except Exception as e:
            print(f" Corrupt index found, starting fresh. Error: {e}")
    else:
        print("Starting with empty AI memory (No index found).")