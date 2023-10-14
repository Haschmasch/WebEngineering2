from setup_database import SessionLocal, engine
from API.Crud import Users, Offers, Categories, Subcategories, Chats
import init_database
from API.Schemas import User, Offer, Category, Subcategory, Chat
from setup_api import run_api
import datetime

from Utils.ConfigManager import configuration


def main():
    init_database.init_db()
    run_api()


if __name__ == "__main__":
    main()
