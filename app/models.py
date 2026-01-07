from sqlalchemy import Column, String, Text, ForeignKey #defines column in DB table, python attribute->DB col
#variable length text column, VARCHAR in MySQL
#large text field,when content is long, TEXT in MySQL
#creates a DB level relationship

from app.database import Base

#All ORM models must inherit from it, SQLAlchemy uses it to: track tables, generate schemas, enforce constraints

class User(Base): #database table model
    __tablename__ = "users" #explicitly names the table
    
    id = Column(String(50),primary_key = True) 
    name = Column(String(100), nullable = False, unique = True)
    
class Document(Base): #represents a document entity
    __tablename__ = "documents"
    
    id = Column(String(50),primary_key = True)
    title = Column(String(200), nullable = False)
    content = Column(Text, nullable = False)
    owner_id=Column(String(50),ForeignKey("users.id"),nullable = False) # owner_id must reference users.id
    
    