from app.core.env import *
from fastapi import FastAPI
from app.database import Base,engine
from app.routers import users,documents,indexing, search
from app.routers.ai import ai_router
from app.services.vector_store import load_index

import os
#creates fastAPI application instance
app = FastAPI(
    title="Document Management API",
    version="2.0"
)

@app.on_event("startup")
def startup_event():
    # 1. Initialize DB tables (keep this)
    Base.metadata.create_all(bind=engine)
    
    # 2. Load the Vector Store from disk
    load_index()
    

#Register (include) user related APIs
#POST /users
#GET /users/{user_id}/documents
app.include_router(users.router)

#Register (include) document related APIs
#POST /documents
app.include_router(documents.router)

#POST /document/index
app.include_router(indexing.router, tags=["Indexing"])

#POST /search
app.include_router(search.router, tags=["Search"])

#POST /ai/ask
app.include_router(ai_router)
