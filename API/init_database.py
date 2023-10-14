import models
from setup_database import engine


def init_db():
    models.Base.metadata.create_all(bind=engine)

