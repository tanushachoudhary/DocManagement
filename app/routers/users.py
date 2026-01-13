from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status 
#APIRouter → lets you group related endpoints
#Depends → FastAPI’s dependency injection system
#HTTPException → return proper HTTP error responses
#status → readable HTTP status codes (201, 400, etc.)

from app.models import User, Document

from sqlalchemy.orm import Session
from app.database import SessionLocal #SessionLocal creates a database session
from app import crud,schemas
# crud → database operations
# schemas → request/response validation (Pydantic)
from typing import List
from app.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])
# Creates a router
# All endpoints here start with: /users

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# FastAPI automatically:
# Opens session
# Injects it
# Closes it
# production-grade DB handling


#POST /users
# @router.post("",status_code=status.HTTP_201_CREATED)
# def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
#     try:
#         return crud.create_user(db,user) #Inserts user into database
#     except:
#         raise HTTPException(status_code=400,detail="User already exists") #Handles duplicate user IDs and Returns proper HTTP error

@router.post("", status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.id == user.id).first()

    if existing:
        return existing

    new_user = User(id=user.id, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# user → validated request body
# db → injected DB session

#GET /users/{user_id}/documents
@router.get("/{user_id}/documents", response_model=List[schemas.DocumentResponse])
def get_documents(user_id: str, db: Session = Depends(get_db)):
    
    # 2. Call the CRUD function
    documents = crud.get_user_documents(db, user_id)
    
    # 3. Safety check: Ensure it returns an empty list, not None
    if documents is None:
        return []
        
    return documents
