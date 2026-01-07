from pydantic import BaseModel,Field #pydantic handles request validation, data parsing, automatic error response
# BaseModel--> base class for schemas
# Field--> adds constraint and metadata

#request body for POST /users
class UserCreate(BaseModel):
    id:str = Field(..., min_length = 1) #... required field
    name:str = Field(..., min_length = 1) # min_length = 1 cannot be empty
    
    
#request body for POST /documents
class DocumentCreate(BaseModel):
    id:str
    title:str
    content:str
    owner_id:str

#used for GET /users/{user_id}/documents
#Controls what data is returned
# Prevents leaking internal fields
class DocumentResponse(BaseModel):
    id:str
    title:str
    content:str
    
    #SQLAlchemy object → JSON automatically
    #Allows Pydantic to read data from: SQLAlchemy ORM objects not just dictionaries
    class Config:
        orm_mode=True