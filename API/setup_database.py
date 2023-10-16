from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from API.Utils.ConfigManager import configuration

engine = create_engine(configuration.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
