from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud,schemas

router = APIRouter(prefix="/documents", tags=["documents"])


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("",status_code=status.HTTP_201_CREATED)
def create_document(doc:schemas.DocumentCreate, db:Session=Depends(get_db)):
    try:
        return crud.create_document(db,doc)
    except:
        raise HTTPException(status_code=400,detail="Invalid owner or duplicate document")