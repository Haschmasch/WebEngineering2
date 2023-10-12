from database import SessionLocal, engine, config
from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from API import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def run_api():
    print("Starting HTTP server in run_api()", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)