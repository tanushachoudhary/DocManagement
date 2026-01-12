from fastapi import APIRouter
import numpy as np
from app.services.embeddings import generate_embedding
from app.services.vector_store import index_document, document_ids


router=APIRouter()

@router.post("/documents/index")
def index_document_api(doc_id:str,text:str):
    index_document(doc_id, text)
    return {"message": "Document indexed successfully"}
    