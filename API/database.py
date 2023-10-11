from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Utils import FileOperations


# Use this variable to access the configuration file via the key of the variable
config = FileOperations.read_json("config.json")
DB_URL = config["ConnectionString"]          #TODO: change to own database url

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


