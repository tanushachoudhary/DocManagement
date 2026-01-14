# Semantic search router module
# Handles vector similarity search across indexed document chunks

from fastapi import APIRouter
# APIRouter: groups related endpoints for modular organization

from pydantic import BaseModel
# BaseModel: base class for creating validated data schemas

from typing import List
# Type hint for list types in response models

from app.services.vector_store import similarity_search
# Import vector store service function that queries FAISS index

# Create router without prefix (endpoint will be /search)
# No tags specified - can be added if grouping multiple search endpoints
router = APIRouter()


# Pydantic models define the JSON structure for API responses
# These ensure consistent, validated output and auto-generate OpenAPI docs

class SearchResult(BaseModel):
    """
    Single search result containing a text chunk and its metadata.
    
    Represents one document chunk that matched the search query.
    """
    text: str  # The actual text content of the chunk
    metadata: dict  # Associated metadata (document_id, chunk_id, filename, etc.)


class SearchResponse(BaseModel):
    """
    Complete search response containing multiple results.
    
    Wraps the list of search results in a structured format.
    """
    results: List[SearchResult]  # Array of SearchResult objects

# POST /search - Semantic search endpoint
@router.post("/search", response_model=SearchResponse)
# @router.post() → HTTP POST method (query passed in request body or as parameter)
# "/search" → URL path for this endpoint
# response_model → FastAPI validates response matches SearchResponse schema
def semantic_search(query: str, k: int = 5):
    """
    Performs semantic vector similarity search across indexed documents.
    Does NOT use an LLM to generate answers - returns raw matching chunks.
    
    This is pure vector search using FAISS:
    1. Converts query text to embedding vector
    2. Finds k most similar document chunks by cosine similarity
    3. Returns matching chunks with their metadata
    
    Args:
        query: The search text (e.g., "invoice total", "project deadline")
               Natural language queries work best
        k: Number of results to return (default: 5)
           Higher values return more results but may include less relevant matches
           
    Returns:
        SearchResponse: JSON object with results array containing text chunks and metadata
        
    Example response:
        {
            "results": [
                {
                    "text": "The invoice total is $1,234.56...",
                    "metadata": {"document_id": 123, "chunk_id": 5, "filename": "invoice.pdf"}
                },
                ...
            ]
        }
    """
    # Call the FAISS vector store wrapper service
    # This function:
    # 1. Embeds the query using the same model that embedded the documents
    # 2. Performs similarity search in FAISS index
    # 3. Returns k most similar chunks with their metadata
    results = similarity_search(query, k=k)
    
    # Format the raw vector store output into API response structure
    # Transform internal format to user-facing JSON schema
    formatted_results = [
        {
            "text": doc["content"],  # The actual text chunk from the document
            "metadata": doc["metadata"]  # Contains document_id, chunk_id, filename, etc.
        }
        for doc in results  # Iterate through all search results
    ]

    # Return formatted response (FastAPI auto-validates against SearchResponse schema)
    # FastAPI converts this dict to JSON automatically
    return {"results": formatted_results}