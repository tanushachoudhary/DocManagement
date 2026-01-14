"""
Indexing Router Module
This module provides API endpoints for manual document indexing operations.
It allows external systems to index documents into the vector store for AI/RAG capabilities.
The primary use case is to manually trigger document indexing when documents are created
through alternative paths (not through the standard upload endpoint).
"""
from fastapi import APIRouter, HTTPException, status
from app.services.document_store import index_document
from app.services.vector_store import save_index
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)

# Initialize the router ONLY ONCE
# This router is mounted at the application level to handle all indexing endpoints
router = APIRouter()

# --- Endpoint: Manual Indexing ---
@router.post("/documents/index")
def index_document_api(doc_id: str, text: str):
    """
    Manually index a string of text under a specific document ID.
    This endpoint allows external systems to trigger document indexing without going
    through the full upload pipeline. Useful for:
    - Re-indexing existing documents
    - Indexing documents from alternative sources
    - Batch indexing operations

    Args:
        doc_id (str): Unique identifier for the document to be indexed
        text (str): The text content to index and chunk for vector search
        
    Returns:
        dict: Success message confirming document indexing
        
    Raises:
        HTTPException: 500 Internal Server Error if indexing fails
        
    Process:
    1. Validates input parameters (doc_id and text)
    2. Calls index_document to split text into chunks and generate embeddings
    3. Saves the vector index to disk for persistence
    """
    try:
        logger.info(f"Starting manual indexing for document: {doc_id}")
        
        # Validate that we have content to index
        if not text or not text.strip():
            logger.warning(f"Empty text provided for document {doc_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text content cannot be empty"
            )
        
        if not doc_id or not doc_id.strip():
            logger.warning("Empty document ID provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document ID cannot be empty"
            )
        
        # Index the document text (splits into chunks and creates embeddings)
        logger.info(f"Indexing {len(text)} characters for document {doc_id}")
        index_document(doc_id, text)
        
        # Persist the vector index to disk
        logger.info("Persisting indexed document to vector store")
        save_index()
        
        logger.info(f"Successfully indexed document: {doc_id}")
        return {"message": "Document indexed successfully", "document_id": doc_id}
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        logger.error(f"Validation error while indexing document {doc_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Indexing validation failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error while indexing document {doc_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to index document"
        )

