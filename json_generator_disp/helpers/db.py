import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = os.getenv("DB_HOST")
user = os.getenv("DB_USERNAME")
passwd = os.getenv("DB_PASS")

Base = declarative_base()

def get_db(db_name: str) -> Generator:
    """Get a DB session
    Yields:
        Generator: A sessionmaker instance
    """
    try:
        DATABASE_URL = f"mysql+pymysql://{user}:{passwd}@{host}/{db_name}"
        engine = create_engine(DATABASE_URL)
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = session_local()
        yield db
    finally:
        db.close()
