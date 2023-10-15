from API.setup_database import SessionLocal
from API.Crud import Offers, Chats
from API.init_database import init_db
from API.Schemas import Offer, Chat
from API.setup_api import run_api
from API.init_database import init_db


def main():
    init_db()
    run_api()


if __name__ == "__main__":
    main()
