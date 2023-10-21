"""
This establishes the database connection and provides functionalities to get the current database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from API.Utils.ConfigManager import configuration

engine = create_engine(configuration.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Gets the current database session.
    :return: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
