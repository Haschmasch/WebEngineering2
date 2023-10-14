from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from API.Endpoints.Chats import router as chat_router
from API.Endpoints.Search import router as search_router
from API.Endpoints.Categories import router as category_router
from API.Endpoints.Subcategories import router as subcategory_router
from API.Endpoints.Users import router as user_router
from API.Endpoints.Offers import router as offer_router

routers = [chat_router, search_router, category_router, subcategory_router, user_router, offer_router]
app = FastAPI()
for router in routers:
    app.include_router(router)


def run_api():
    print("Starting HTTP server in run_api()", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)
