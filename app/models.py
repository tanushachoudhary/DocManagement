from sqlalchemy import Column, String, Text
#variable length text column, VARCHAR in MySQL
#large text field,when content is long, TEXT in MySQL
from sqlalchemy import ForeignKey
from app.database import Base

#All ORM models must inherit from it, SQLAlchemy uses it to: track tables, generate schemas, enforce constraints

class User(Base): #database table model
    __tablename__ = "users" #explicitly names the table
    
    id = Column(String(50),primary_key = True) 
    name = Column(String(100), nullable = False, unique = True)
    
class Document(Base): #represents a document entity
    __tablename__ = "documents"
    
    id = Column(String(50), primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    owner_id = Column(String(50), ForeignKey("users.id"), index=True)
    extracted_text = Column(Text, nullable=True)
    
    
