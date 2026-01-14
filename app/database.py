from sqlalchemy import create_engine #creates a DB connection interface(bridge between python and DB)
from sqlalchemy.orm import sessionmaker,declarative_base #creates DB session(opens DB connection, track changes to obj, commits/rolls back transaction)
#declarative_base--> creates base class for ORM models(keeps metadata about tables,columns,constraints)(python classes->DB tables)

import os

# 1. Fetching credentials from Environment Variables (with defaults for safety)
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password") 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "docdb")
DB_PORT = os.getenv("DB_PORT", "3306")

# 2. Constructing the Connection URL dynamically
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DB_URL = "mysql+pymysql://root:tanushac1811@:3306/docdb"

engine=create_engine(DB_URL,echo=True)
# Creates the SQLAlchemy Engine
# Handles: DB driver (pymysql), connection pooling, SQL compilation

SessionLocal= sessionmaker(bind=engine,autoflush=False,autocommit=False)
# Creates a session factory
# Every request creates a new session:
# db = SessionLocal()
# Each API request: gets its own DB session, is isolated, can safely commit or rollback, prevents data corruption.

Base=declarative_base()
#creates base class for ORM models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
