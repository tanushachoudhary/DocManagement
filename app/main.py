from fastapi import FastAPI
from app.database import Base,engine
from app.routers import users,documents,indexing, search

#creates all DB tables defined using SQLAlchemy models
#this checks if tables already exist and creates them if they don't
Base.metadata.create_all(bind=engine)

#creates fastAPI application instance
app = FastAPI(
    title="Document Management API",
    version="2.0"
)


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