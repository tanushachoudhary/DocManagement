from fastapi import APIRouter
import numpy as np
# We import the helper functions from our service layer
from app.services.embeddings import generate_embedding
from app.services.vector_store import index_document, document_ids

router = APIRouter()

# POST /documents/index
# This endpoint is used to manually add a document to the vector store.
@router.post("/documents/index")
def index_document_api(doc_id: str, text: str):
    """
    Receives a document ID and text.
    Passes it to the service layer to be converted into a vector and stored.
    """
    # Calls the function in app/services/vector_store.py
    # This creates the embedding and appends it to the lists.
    index_document(doc_id, text)
    
    return {"message": "Document indexed successfully"}