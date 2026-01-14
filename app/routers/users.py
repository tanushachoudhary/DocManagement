import logging
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status 
#APIRouter → lets you group related endpoints
#Depends → FastAPI's dependency injection system
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

# Configure logger
logger = logging.getLogger(__name__)


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
@router.post("", status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Attempting to create user with ID: {user.id}")
        
        existing = db.query(User).filter(User.id == user.id).first()

        if existing:
            logger.warning(f"User with ID {user.id} already exists, returning existing user")
            return existing

        new_user = User(id=user.id, name=user.name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"Successfully created user with ID: {user.id}")
        return new_user
        
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error while creating user {user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this ID already exists or invalid data provided"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating user {user.id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


# user → validated request body
# db → injected DB session

#GET /users/{user_id}/documents
@router.get("/{user_id}/documents", response_model=List[schemas.DocumentResponse])
def get_documents(user_id: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching documents for user: {user_id}")
        
        # 2. Call the CRUD function
        documents = crud.get_user_documents(db, user_id)
        
        # 3. Safety check: Ensure it returns an empty list, not None
        if documents is None:
            logger.warning(f"No documents found for user {user_id}, returning empty list")
            return []
        
        logger.info(f"Successfully retrieved {len(documents)} documents for user: {user_id}")
        return documents
        
    except ValueError as e:
        logger.error(f"Invalid user ID format: {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error fetching documents for user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve documents"
        )
