from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ocr import extract_text
from app.models import Document
from app import crud, schemas
# Services for the "RAG" part (Chunking & Indexing)
from app.services.document_store import index_document
from app.services.vector_store import save_index
from sqlalchemy.exc import IntegrityError

import shutil
import os
import uuid

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#POST /documents
# app/routers/documents.py

# 1. Update response_model to use the new schema
@router.post("", status_code=201, response_model=schemas.DocumentCreateResponse)
def create_document(doc: schemas.DocumentCreate, db: Session = Depends(get_db)):
    try:
        # 2. Create the document using CRUD
        new_doc = crud.create_document(db, doc)
        
        # 3. Return a dictionary that matches DocumentCreateResponse
        return {
            "id": new_doc.id,
            "filename": new_doc.filename,
            "content": new_doc.content,
            "extracted_text": new_doc.extracted_text,
            "owner_id": new_doc.owner_id,
            "message": "Document created successfully"  # <--- The message you wanted
        }

    except IntegrityError:
        raise HTTPException(
            status_code=400, 
            detail="Operation failed. User does not exist or Document ID is duplicate."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# POST /documents/upload (The Full Pipeline)
@router.post("/upload", status_code=201)
def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),  # Received as Form data since we are uploading a file
    db: Session = Depends(get_db)
):
    """
    Handles the full document lifecycle:
    1. Validation: Checks file type.
    2. Storage: Saves file to local disk.
    3. Processing: Runs OCR to extract text.
    4. Database: Saves metadata and text to SQL.
    5. AI Indexing: Chunks text and saves to Vector Store.
    """
    
    # 1. Validate file type
    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported File Type")
    
    # --- STEP 2: SAVE TO DISK ---
    # We generate a UUID to prevent filename collisions (e.g., two users uploading "invoice.pdf")
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {e}")
        
    # --- STEP 3: OCR EXTRACTION ---
    try:
        # Extract raw text from the binary file
        extracted_text = extract_text(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
    
    # Fail fast if the document is empty/blank
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from this file.")

    # --- STEP 4: SQL STORAGE (METADATA) ---
    document = Document(
        id=file_id,
        filename=file.filename,
        extracted_text=extracted_text,
        owner_id=user_id      
    )
    
    try:
        db.add(document)
        db.commit()      # Save transaction
        db.refresh(document) # Refresh instance with DB data
    except Exception as e:
        db.rollback()    # Undo changes if DB write fails
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # --- STEP 5: VECTOR INDEXING (THE AI MEMORY) ---
    # This splits the text into chunks and converts them to vectors
    try:
        index_document(document.id, document.extracted_text)
    except Exception as e:
        # We log the error but don't fail the request, because the data is safe in SQL.
        # In a real app, you might add this to a "retry queue".
        print(f"Indexing Error: {e}")

    # --- STEP 6: PERSISTENCE ---
    # Save the vector index to disk so it survives server restarts
    save_index()

    return {
        "id": document.id,           # Matches schema 'id'
        "owner_id": document.owner_id,
        "extracted_text": extracted_text,
        "extracted_text_length": len(extracted_text),
        "message": "File uploaded, saved to DB, indexed, and persisted."
    }

# Uncomment this endpoint during debugging to verify chunking logic
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