from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from dateutil.parser import parse
from API.setup_database import get_db
from API.Search.Search import search_offers

router = APIRouter()


@router.get("/search/")
def search(
        query: str = None,
        category_id: int = None,
        subcategory_id: int = None,
        location: str = None,
        min_price: float = None,
        max_price: float = None,
        min_date: str = None,
        max_date: str = None,
        db: Session = Depends(get_db)
):
    # parse the date strings
    min_date = parse(min_date) if min_date else None
    max_date = parse(max_date) if max_date else None

    # perform search
    results = search_offers(
        db, query, category_id, subcategory_id, location,
        min_price, max_price, min_date, max_date
    )

    return results