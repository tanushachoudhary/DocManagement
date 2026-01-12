from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.vector_store import similarity_search

router = APIRouter()

# Response Models maintain consistent JSON structure
class SearchResult(BaseModel):
    text: str
    metadata: dict

class SearchResponse(BaseModel):
    results: List[SearchResult]

@router.post("/search", response_model=SearchResponse)
def semantic_search(query: str, k: int = 5):
    """
    Performs purely semantic search (Vector similarity).
    Does NOT use an LLM to generate answers.
    
    Args:
        query: The raw text to search for (e.g. "invoice total")
        k: How many results to return (Default: 5)
    """
    # Call the FAISS wrapper service
    results = similarity_search(query, k=k)
    
    # Format the raw output for the frontend
    formatted_results = [
        {
            "text": doc["content"], # The actual text chunk
            "metadata": doc["metadata"] # Contains doc_id, filename, etc.
        }
        for doc in results
    ]

    return {"results": formatted_results}