from fastapi import APIRouter, Depends, HTTPException, status
#APIRouter → lets you group related endpoints
#Depends → FastAPI’s dependency injection system
#HTTPException → return proper HTTP error responses
#status → readable HTTP status codes (201, 400, etc.)
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud,schemas
# crud → database operations
# schemas → request/response validation (Pydantic)

router = APIRouter(prefix="/documents", tags=["documents"])
# Creates a router
# All endpoints here start with: /documents

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
#POST /documents
@router.post("",status_code=status.HTTP_201_CREATED)
def create_document(doc:schemas.DocumentCreate, db:Session=Depends(get_db)):
    try:
        return crud.create_document(db,doc) #inserts doc into database
    except:
        raise HTTPException(status_code=400,detail="Invalid owner or duplicate document") #Converts DB errors into proper HTTP responses