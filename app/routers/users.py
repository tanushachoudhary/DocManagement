from fastapi import APIRouter, Depends, HTTPException, status 
#APIRouter--> 
#Depends-->
#HTTPException-->
#status-->
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud,schemas

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("",status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    try:
        return crud.create_user(db,user)
    except:
        raise HTTPException(status_code=400,detail="User already exists")

@router.get("/{user.id}/documents")
def get_documents(user_id:str, db:Session=Depends(get_db)):
    return crud.get_user_documents(db,user_id)