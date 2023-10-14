from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy import select
from API import models


def search_by_category(db: Session, category_id: int = None, subcategory_id: int = None):
    conditions = []

    if category_id:
        conditions.append(models.Offer.categoryid == category_id)

    if subcategory_id:
        conditions.append(models.Offer.subcategoryid == subcategory_id)

    return conditions


def search_by_location(db: Session, location: str = None, postcode: str = None):
    conditions = []

    if location:
        conditions.append(models.Offer.city == location)

    if postcode:
        conditions.append(models.Offer.postcode == postcode)

    return conditions


def extended_search(db: Session, min_price: float = None, max_price: float = None, min_date=None, max_date=None):
    conditions = []

    if min_price:
        conditions.append(models.Offer.price >= min_price)

    if max_price:
        conditions.append(models.Offer.price <= max_price)

    if min_date:
        conditions.append(models.Offer.timeposted >= min_date)

    if max_date:
        conditions.append(models.Offer.timeposted <= max_date)

    return conditions


def search_offers(db: Session, query: str = None, category_id: int = None, subcategory_id: int = None,
                  location: str = None, postcode: str = None, min_price: float = None, max_price: float = None,
                  min_date=None, max_date=None):

    base_query = select(models.Offer)

    # get conditions from sub-search functions
    conditions = []
    conditions.extend(search_by_category(db, category_id, subcategory_id))
    conditions.extend(search_by_location(db, location, postcode))
    conditions.extend(extended_search(db, min_price, max_price, min_date, max_date))

    # text query condition
    if query:
        conditions.append(models.Offer.title.contains(query))

    # combine conditions
    if conditions:
        base_query = base_query.where(and_(*conditions))

    result = db.execute(base_query)

    return result.all()

