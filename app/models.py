# SQLAlchemy ORM models - defines database table structures
# These models map Python classes to database tables

from sqlalchemy import Column, String, Text
# Column: defines a database column
# String: variable length text column, VARCHAR in SQL
# Text: large text field for long content, TEXT in SQL

from sqlalchemy import ForeignKey
# ForeignKey: creates a relationship link between tables

from app.database import Base
# Base: declarative base class that all ORM models must inherit from
# SQLAlchemy uses it to: track tables, generate schemas, enforce constraints

class User(Base):
    """
    User ORM model - represents the users table in the database
    Stores user account information
    """
    __tablename__ = "users"  # explicitly names the database table
    
    # Primary key: unique identifier for each user (max 50 characters)
    id = Column(String(50), primary_key=True) 
    
    # User's name: required field, must be unique across all users (max 100 characters)
    name = Column(String(100), nullable=False, unique=True)
    
class Document(Base):
    """
    Document ORM model - represents the documents table in the database
    Stores uploaded document metadata and extracted text content
    """
    __tablename__ = "documents"
    
    # Primary key: unique identifier for each document, indexed for fast lookups
    id = Column(String(50), primary_key=True, index=True)
    
    # Original filename: required field (max 255 characters)
    filename = Column(String(255), nullable=False)
    
    # Foreign key linking to User.id: establishes ownership relationship
    # Indexed for fast queries like "get all documents by user"
    owner_id = Column(String(50), ForeignKey("users.id"), index=True)
    
    # Extracted text content: optional field for OCR/text extraction results
    # Uses Text type to handle large amounts of text
    extracted_text = Column(Text, nullable=True)