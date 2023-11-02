from init_database import init_db
from setup_api import run_api


def main():
    init_db()
    run_api()


if __name__ == "__main__":
    main()
