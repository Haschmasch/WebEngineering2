"""
Functionalities for initializing the database using the sqlalchemy models.
"""

import models
from setup_database import engine
from sqlalchemy import event
from sqlalchemy_utils import database_exists, create_database
from Utils.FileOperations import read_json

TABLE_DATA = read_json("./Utils/init_table_data.json")


def init_db():
    """
    Initializes the database if it does net exist and the database tables afterwards.
    """
    if not engine.url.username == "postgres":
        print("To create the database the superuser 'postgres' needs to be used in the connection string. Otherwise "
              "the database needs to be created manually.")
    if not database_exists(engine.url) and engine.url.username == "postgres":
        create_database(engine.url)
    models.Base.metadata.create_all(bind=engine)


def seed_tables(target, connection, **kw):
    """
    Seeds the database tables with initial data from a json file.
    :param target: Target table
    :param connection: DB connection
    :param kw: Dunno
    """
    table_name = str(target)
    if table_name in TABLE_DATA and len(TABLE_DATA[table_name]) > 0:
        connection.execute(target.insert(), TABLE_DATA[table_name])


# The Events for the individual tables that are seeded are subscribed here
@event.listens_for(models.User.__table__, 'after_create')
def user_after_create(target, connection, **kw):
    seed_tables(target, connection, **kw)


@event.listens_for(models.Offer.__table__, 'after_create')
def user_after_create(target, connection, **kw):
    seed_tables(target, connection, **kw)


@event.listens_for(models.Category.__table__, 'after_create')
def user_after_create(target, connection, **kw):
    seed_tables(target, connection, **kw)


@event.listens_for(models.Subcategory.__table__, 'after_create')
def user_after_create(target, connection, **kw):
    seed_tables(target, connection, **kw)


@event.listens_for(models.Following.__table__, 'after_create')
def user_after_create(target, connection, **kw):
    seed_tables(target, connection, **kw)


@event.listens_for(models.Chat.__table__, 'after_create')
def user_after_create(target, connection, **kw):
    seed_tables(target, connection, **kw)

