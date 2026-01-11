from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> np.ndarray:
    return model.encode(text, normalize_embeddings=True)
