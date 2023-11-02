"""
Contains the API endpoint for the '/search' route.
"""


import datetime

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from setup_database import get_db
from Search.Search import search_offers
from Schemas import Relations

router = APIRouter(
    prefix="/search",
    tags=["search"])


@router.get("/", response_model=list[Relations.OfferWithRelations])
def search(
        db: Session = Depends(get_db),
        query: str | None = None,
        category_id: int | None = None,
        subcategory_id: int | None = None,
        location: str | None = None,
        postcode: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_date: datetime.datetime | None = None,
        max_date: datetime.datetime | None = None,
):
    # perform search
    results = search_offers(
        db, query, category_id, subcategory_id, location, postcode,
        min_price, max_price, min_date, max_date)
    return results
