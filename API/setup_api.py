"""
Includes setup functionalities for the API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Endpoints.Chats import router as chat_router
from Endpoints.Followings import router as following_router
from Endpoints.Users import router as user_router
from Endpoints.Categories import router as category_router
from Endpoints.Subcategories import router as subcategory_router
from Endpoints.Offers import router as offer_router
from Endpoints.Search import router as search_router

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
app.include_router(search_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def run_api():
    """
    This starts the API using the uvicorn server.
    """
    print("Starting HTTP server in run_api()", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)
