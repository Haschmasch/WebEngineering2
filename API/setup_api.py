from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from API.Endpoints.Chats import router as chat_router
from API.Endpoints.Followings import router as following_router
from API.Endpoints.Users import router as user_router
from API.Endpoints.Categories import router as category_router
from API.Endpoints.Subcategories import router as subcategory_router
from API.Endpoints.Offers import router as offer_router

description = """
This is the backend for the GenuineGoods WebApp.
Basic CRUD (Create, Read, Update, Delete) operations are available for all following routers.

## Categories

## Subcategories

## Chats

## Followings

## Offers

## Users

"""

app = FastAPI(
    title="GenuineGoods API",
    description=description,
    summary="Provides backend functionalities for the GenuineGoods WebApp",
    version="0.0.1",
)
app.include_router(chat_router)
app.include_router(following_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(offer_router)


def run_api():
    print("Starting HTTP server in run_api()", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)
