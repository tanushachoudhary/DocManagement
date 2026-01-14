# User management router module
# Handles user creation and document retrieval for specific users

import logging
# Standard library: provides logging functionality for debugging and monitoring

from sqlalchemy.exc import IntegrityError
# SQLAlchemy exception: raised when database constraints are violated (e.g., duplicate keys)

from fastapi import APIRouter, Depends, HTTPException, status 
# APIRouter → lets you group related endpoints under a common prefix
# Depends → FastAPI's dependency injection system for managing resources
# HTTPException → return proper HTTP error responses with status codes
# status → readable HTTP status codes (201 Created, 400 Bad Request, etc.)

from app.models import User
# Import the User ORM model (SQLAlchemy table definition)

from sqlalchemy.orm import Session
# SQLAlchemy Session: manages database transactions and queries

from app.database import SessionLocal
# SessionLocal: factory function that creates database sessions

from app import crud, schemas
# crud → database operations (create, read, update, delete functions)
# schemas → Pydantic models for request/response validation

from typing import List
# Type hint for list return types

from app.database import get_db
# Dependency function that provides database sessions to route handlers

# Configure logger for this module
# __name__ ensures log messages show the correct module name
logger = logging.getLogger(__name__)

# Create API router with common configuration
router = APIRouter(prefix="/users", tags=["Users"])
# prefix="/users" → All routes in this router start with /users (e.g., /users, /users/{user_id}/documents)
# tags=["Users"] → Groups these endpoints under "Users" in API documentation (Swagger UI)


def get_db():
    """
    Database session dependency generator.
    
    This function provides a database session to route handlers and ensures proper cleanup.
    FastAPI's dependency injection automatically:
    1. Opens a new session before the request
    2. Injects it into route handlers that declare db: Session = Depends(get_db)
    3. Closes the session after the request completes (even if errors occur)
    
    This is production-grade DB handling that prevents connection leaks.
    """
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session to the route handler
        # The code pauses here while the route executes
        yield db
    finally:
        # Always close the session after the request completes
        # This runs even if an exception occurred
        db.close()


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
# @router.get() → HTTP GET method
# "/{user_id}/documents" → URL path with dynamic parameter (e.g., /users/user123/documents)
# response_model → Validates/serializes response as list of DocumentResponse objects
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
