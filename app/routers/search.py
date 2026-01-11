from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

# Import the search logic from your existing service
from app.services.vector_store import similarity_search

router = APIRouter()

# Define a response model for clarity
class SearchResult(BaseModel):
    text: str
    metadata: dict

@router.post("/search", response_model=dict)
def semantic_search(query: str):
    # Delegate the work to the vector_store service
    results = similarity_search(query)
    
    # Format the results for the API response
    formatted_results = [
        {
            "text": doc["content"],
            "metadata": doc["metadata"]
        }
        for doc in results
    ]

    return {"results": formatted_results}