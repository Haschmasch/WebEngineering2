from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from Crud import *
from Schemas import *
import models
from database import SessionLocal, engine
import uvicorn


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def run_api():
    print("Starting HTTP server in run_api()", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def main():
    print("Hallo")


if __name__ == "__main__":
    main()
