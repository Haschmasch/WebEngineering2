from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import Crud.Users
from API.Crud import Users
from API.Schemas import User
from API import models
from database import SessionLocal, engine, config
import uvicorn
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def run_api():
    print("Starting HTTP server in run_api()", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)


def main():
    # Hier kann man was zum testen rein schreiben. Später kommt hier nur run_api() rein.
    createUser = User.UserCreate(email="m.m@example.com",
                                 name="test",
                                 phone_number="1681561",
                                 timecreated=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
                                 password="123456")
    db = SessionLocal()
    Users.create_user(db, createUser)
    db.close()
    print("Hallo")


if __name__ == "__main__":
    main()
