from fastapi import FastAPI
from app.database import Base,engine
from app.routers import users,documents

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



# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)

# app.include_router(users.router)
# app.include_router(documents.router)
