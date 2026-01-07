from sqlalchemy.orm import Session #represents a DB transaction
from app import models 
# Imports ORM models:
# models.User
# models.Document
# map Python objects → database tables

def create_user(db:Session, user):#db → active SQLAlchemy session
    #user → validated Pydantic schema (UserCreate)
    db_user = models.User(**user.dict()) 
    #user.dict() converts Pydantic model → Python dictionary
    # ** unpacks the dictionary
    # Creates a User ORM object
    db.add(db_user) #Marks object for insertion
    db.commit() #Executes SQL INSERT
    # Persists data permanently
    # Ends transaction
    return db_user #FastAPI + Pydantic (orm_mode) converts it to JSON
    # No manual serialization needed


def create_document(db:Session, doc): #Accepts validated document input
    # Uses ORM model
    db_doc=models.Document(**doc.dict())
    db.add(db_doc)
    db.commit()
    return db_doc

def get_user_documents(db:Session, user_id:str): #Fetch all documents owned by a user
    return db.query(models.Document).filter(
        models.Document.owner_id == user_id
    ).all()
    
    #SELECT * FROM documents WHERE owner_id = :user_id;
    #.all() Executes query
    # Returns a list of ORM objects