from API import setup_database
from API.Crud import Offers
from API.Schemas import Offer
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import exc

from API.Utils.ConfigManager import configuration

router = APIRouter()


@router.post("/offers/", response_model=Offer.Offer, status_code=status.HTTP_201_CREATED)
def add_category(offer: Offer.OfferCreate, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.create_offer(db, offer, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.put("/offers/", response_model=Offer.Offer)
def update_user(offer: Offer.Offer, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.update_offer(db, offer, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.delete("/offers/", response_model=Offer.Offer)
def delete_category(offer_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.delete_offer(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/offers/{offer_id}", response_model=Offer.Offer)
def get_user(offer_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.get_offer(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)

'''
@router.get("/offers/{offer_id}/relations", response_model=Offer.OfferWithRelations)
def get_category_with_offers(offer_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.get_offer(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@router.get("/offers/", response_model=list[Offer.OfferWithRelations])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.get_offers(db, skip, limit, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


# TODO: Implement
@router.get("/offers/{offer_id}/images", response_model=list[Offer.OfferWithRelations])
def get_image(offer_id: int, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    pass


@router.post("/offers/{offer_id}/images", response_model=list[Offer.OfferWithRelations])
def create_image(offer_id: int, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    pass


# TODO: Implement
@router.get("/offers/{offer_id}/images/{image_id}", response_model=list[Offer.OfferWithRelations])
def get_users(offer_id: int, image_id: int, db: Session = Depends(setup_database.get_db)):
    pass
'''

