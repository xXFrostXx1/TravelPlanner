from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()

def get_database_url():
    return os.getenv("DATABASE_URL")

def create_engine_connection(database_url):
    return create_engine(database_url)

def create_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

load_environment_variables()
DATABASE_URL = get_database_url()
engine = create_engine_connection(DATABASE_URL)
SessionLocal = create_session_local(engine)

if __name__ == "__main__":
    print("Database setup module executed.")