from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_environment_variables():
    try:
        load_dotenv()
    except Exception as e:
        logging.error("Failed to load the environment variables: {}", e)
        raise e

def get_database_url():
    try:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL is not set in the environment variables.")
        return db_url
    except Exception as e:
        logging.error("Failed to get database URL: {}", e)
        raise e

def create_engine_connection(database_url):
    try:
        engine = create_engine(database_url)
        return engine
    except exc.SQLAlchemyError as sql_err:
        logging.error("Failed to create an engine: {}", sql_err)
        raise sql_err
    except Exception as e:
        logging.error("Unexpected error when creating an engine: {}", e)
        raise e

def create_session_local(engine):
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal
    except Exception as e:
        logging.error("Failed to create a sessionmaker instance: {}", e)
        raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error("Error during session operation: {}", e)
        raise e
    finally:
        db.close()

try:
    load_environment_variables()
    DATABASE_URL = get_database_url()
    engine = create_engine_connection(DATABASE_URL)
    SessionLocal = create_session_local(engine)
except Exception as e:
    logging.critical("Failed to start the database connection: {}", e)
    exit(1)

if __name__ == "__main__":
    logging.info("Database setup module executed successfully.")