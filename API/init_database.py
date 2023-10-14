from API import models
from API.setup_database import engine


def init_db():
    models.Base.metadata.create_all(bind=engine)

