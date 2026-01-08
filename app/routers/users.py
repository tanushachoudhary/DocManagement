from fastapi import APIRouter, Depends, HTTPException, status 
#APIRouter → lets you group related endpoints
#Depends → FastAPI’s dependency injection system
#HTTPException → return proper HTTP error responses
#status → readable HTTP status codes (201, 400, etc.)

from sqlalchemy.orm import Session
from app.database import SessionLocal #SessionLocal creates a database session
from app import crud,schemas
# crud → database operations
# schemas → request/response validation (Pydantic)

router = APIRouter(prefix="/users", tags=["users"])
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
@router.post("",status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    try:
        return crud.create_user(db,user) #Inserts user into database
    except:
        raise HTTPException(status_code=400,detail="User already exists") #Handles duplicate user IDs and Returns proper HTTP error

# user → validated request body
# db → injected DB session


#GET /users/{user_id}/documents
@router.get("/{user.id}/documents")
def get_documents(user_id:str, db:Session=Depends(get_db)): #user id comes from url and db is injected
    return crud.get_user_documents(db,user_id) #Fetches all documents owned by the user
    # Returns a list (FastAPI auto-serializes)