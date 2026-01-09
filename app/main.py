from fastapi import FastAPI
from app.database import Base,engine
from app.routers import users,documents

import os
#creates fastAPI application instance
app = FastAPI(
    title="Document Management API",
    version="2.0"
)


#creates all DB tables defined using SQLAlchemy models
#this checks if tables already exist and creates them if they don't
@app.on_event("startup")
def on_startup():
    if os.getenv("ENV") != "test":
        Base.metadata.create_all(bind=engine)


#Register (include) user related APIs
#POST /users
#GET /users/{user_id}/documents
app.include_router(users.router)


#Register (include) document related APIs
#POST /documents
app.include_router(documents.router)
