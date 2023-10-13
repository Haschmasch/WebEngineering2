from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Utils.ConfigManager import ConfigManager

#TODO: instantiate ConfigManager as a singleton avoiding circular imports (database.py <> setup.py)
config_manager = ConfigManager()

engine = create_engine(config_manager.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
