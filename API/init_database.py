"""
Functionalities for initializing the database using the sqlalchemy models.
"""

from API import models
from API.setup_database import engine


def init_db():
    """
    Initializes the database tables.
    """
    models.Base.metadata.create_all(bind=engine)

