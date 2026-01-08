from sqlalchemy import create_engine #creates a DB connection interface(bridge between python and DB)
from sqlalchemy.orm import sessionmaker,declarative_base #creates DB session(opens DB connection, track changes to obj, commits/rolls back transaction)
#declarative_base--> creates base class for ORM models(keeps metadata about tables,columns,constraints)(python classes->DB tables)
from dotenv import load_dotenv

load_dotenv()
import os
DB_URL  = os.getenv("DB_URL")

engine=create_engine(DB_URL)
# Creates the SQLAlchemy Engine
# Handles: DB driver (pymysql), connection pooling, SQL compilation

SessionLocal= sessionmaker(bind=engine)
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
