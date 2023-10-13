from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from API.Endpoints.Chats import router as chat_router


app = FastAPI()
app.include_router(chat_router)


def run_api():
    print("Starting HTTP server in run_api()", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)