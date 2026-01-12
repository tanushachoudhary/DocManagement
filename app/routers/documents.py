# app/routers/documents.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ocr import extract_text
from app.models import Document
from app import crud, schemas

# --- NEW IMPORTS REQUIRED FOR AI ---
from app.services.document_store import index_document
from app.services.vector_store import save_index

import shutil
import os
import uuid
from app.services.vector_store import get_chunks_by_doc_id

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# POST /documents (Metadata only)
@router.post("", status_code=201)
def create_document(doc: schemas.DocumentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_document(db, doc)
    except:
        raise HTTPException(status_code=400, detail="Invalid owner or duplicate document")

# POST /documents/upload (The Full Pipeline)
@router.post("/upload", status_code=201)
def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    # 1. Validate file type
    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported File Type")
    
    # 2. Save file to local disk (uploads/ folder)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. OCR extraction
    # Note: Ensure your extract_text function supports file paths!
    # If your ocr.py expects bytes, you might need to read the file again.
    try:
        # Assuming extract_text can handle the file path based on your snippet
        # If it requires bytes, use: extract_text(open(file_path, "rb").read(), file.filename)
        extracted_text = extract_text(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
    
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from this file.")

    # 4. Store in SQL DB
    document = Document(
        id=file_id,
        filename=file.filename,
        extracted_text=extracted_text,
        owner_id=user_id      
    )
    
    try:
        db.add(document)
        db.commit()
        db.refresh(document)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # --- CRITICAL NEW STEPS ---

    # 5. Index the Document (Chunking + Embedding)
    # This adds the text to the in-memory AI brain
    try:
        index_document(document.id, document.extracted_text)
    except Exception as e:
        print(f"Indexing Error: {e}")
        # Optional: You might want to return a warning, but we proceed for now

    # 6. Save Index to Disk (Persistence)
    # This ensures the AI remembers this document if the server restarts
    save_index()

    return {
        "document_id": document.id,
        "owner_id": document.owner_id,
        "extracted_text_length": len(extracted_text),
        "message": "File uploaded, saved to DB, indexed, and persisted."
    }

# @router.get("/{document_id}/chunks")
# def view_document_chunks(document_id: str):
#     """
#     Retrieve the raw text chunks for a specific document.
#     Useful for verifying chunk_size and overlap.
#     """
#     # Note: Ensure get_chunks_by_doc_id treats IDs as strings!
#     chunks = get_chunks_by_doc_id(document_id)
    
#     if not chunks:
#         return {"message": "No chunks found for this document ID."}
        
#     return {
#         "document_id": document_id,
#         "total_chunks": len(chunks),
#         "chunks": chunks
#     }