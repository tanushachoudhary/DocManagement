from pydantic import BaseModel,Field,ConfigDict #pydantic handles request validation, data parsing, automatic error response
# BaseModel--> base class for schemas
# Field--> adds constraint and metadata

from typing import Optional

#request body for POST /users
class UserCreate(BaseModel):
    id:str = Field(..., min_length = 1) #... required field
    name:str = Field(..., min_length = 1) # min_length = 1 cannot be empty
    
    
#request body for POST /documents
class DocumentCreate(BaseModel):
    id:str
    filename:str
    content:str
    owner_id:str

#used for GET /users/{user_id}/documents
#Controls what data is returned
# Prevents leaking internal fields
class DocumentResponse(BaseModel):
    id: str
    filename: str 
    extracted_text: Optional[str] = None 
    owner_id: str
    
    # #SQLAlchemy object → JSON automatically
    # #Allows Pydantic to read data from: SQLAlchemy ORM objects not just dictionaries
    # class Config:
    #     orm_mode=True
    
    model_config = ConfigDict(from_attributes=True)
    

class DocumentUploadCreate(BaseModel):
    id: str
    filename: str
    extracted_text: str
    owner_id: str

class DocumentUploadResponse(BaseModel):
    id: str
    owner_id: str
    extracted_text: Optional[str] = None
    extracted_text_length: int
    message: str
    
    
class DocumentCreateResponse(DocumentResponse):
    message: str