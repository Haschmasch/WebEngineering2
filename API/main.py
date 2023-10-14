from API.setup_database import SessionLocal
from API.Crud import Offers, Chats
from API.init_database import init_db
from API.Schemas import Offer, Chat
from API.setup_api import run_api
import datetime
from API.Utils.ConfigManager import configuration



def main():
    init_database.init_db()
    run_api()


if __name__ == "__main__":
    main()
