from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.vector_store import similarity_search

router = APIRouter()

# 1. Define the model for a SINGLE result
class SearchResult(BaseModel):
    text: str
    metadata: dict

# 2. Define the model for the WHOLE response
class SearchResponse(BaseModel):
    results: List[SearchResult]

@router.post("/search", response_model=SearchResponse)
def semantic_search(query: str, k: int = 5): # <--- Added 'k' parameter
    """
    Perform semantic search over documents.
    query: The text to search for.
    k: Number of results to return (default 5).
    """
    
    # Pass 'k' to the service layer
    results = similarity_search(query, k=k)
    
    formatted_results = [
        {
            "text": doc["content"],
            "metadata": doc["metadata"]
        }
        for doc in results
    ]

    return {"results": formatted_results}