from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
#APIRouter → lets you group related endpoints
#Depends → FastAPI’s dependency injection system
#HTTPException → return proper HTTP error responses

from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ocr import extract_text
from app.models import Document
from app import crud,schemas

import shutil
import os
import uuid

router = APIRouter(prefix="/documents", tags=["documents"])
# Creates a router
# All endpoints here start with: /documents


UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)
        
    
#POST /documents
@router.post("",status_code=201)
def create_document(doc:schemas.DocumentCreate, db:Session=Depends(get_db)):
    try:
        return crud.create_document(db,doc) #inserts doc into database
    except:
        raise HTTPException(status_code=400,detail="Invalid owner or duplicate document") #Converts DB errors into proper HTTP responses        
        
#POST /documents/upload
@router.post("/upload",status_code=201)
def upload_document(
    file: UploadFile = File(...),
    db: Session=Depends(get_db)
):
    #validate file type
    allowed_types=[
        "image/png",
        "image/jpeg",
        "application/pdf",
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code = 400, detail = "Unsupported File Type")
    
    #save file
    file_id=str(uuid.uuid4())
    file_path=os.path.join(UPLOAD_DIR,f"{file_id}_{file.filename}")
    
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
        
    #OCR extraction
    extracted_text=extract_text(file_path)
    
    #Store in DB
    document=Document(
        id=file_id,
        filename=file.filename,
        extracted_text=extracted_text        
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "document_id":document.id,
        "extracted_text":extracted_text
    }
    
