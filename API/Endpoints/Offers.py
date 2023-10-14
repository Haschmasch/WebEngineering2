from API import setup_database
from API.Crud import Offers
from API.Schemas import Offer
from API.Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, APIRouter
from sqlalchemy import exc
from API.Utils.ConfigManager import configuration
from fastapi.responses import Response, FileResponse


router = APIRouter(
    prefix="/offers",
    tags=["offers"]
)


@router.post("/", response_model=Offer.Offer, status_code=status.HTTP_201_CREATED)
def add_offer(offer: Offer.OfferCreate, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.create_offer(db, offer, configuration.offer_root_dir)
    except exc.DatabaseError as db_error:
        raise HTTPException(status_code=400, detail=db_error.detail)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.put("/", response_model=Offer.Offer)
def update_offer(offer: Offer.Offer, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.update_offer(db, offer, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.delete("/", response_model=Offer.Offer)
def delete_offer(offer_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.delete_offer(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.get("/{offer_id}", response_model=Relations.OfferWithRelations)
def get_offer(offer_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.get_offer(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.get("/", response_model=list[Relations.OfferWithRelations])
def get_offers(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.get_offers(db, skip, limit, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.get("/{offer_id}/images", response_class=Response)
def get_offer_images(offer_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Offers.get_offer_images(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.get("/{offer_id}/images/{image_name}")
def get_offer_image(offer_id: int, image_name: str, db: Session = Depends(setup_database.get_db)):
    try:
        image_path = Offers.get_image_path(db, offer_id, image_name, configuration.offer_root_dir)
        return FileResponse(image_path)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=f"File {e.filename} not found")
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.post("/{offer_id}/images", status_code=status.HTTP_201_CREATED)
def create_offer_images(offer_id: int, files: list[UploadFile], db: Session = Depends(setup_database.get_db)):
    try:
        if all("image" in file.content_type for file in files):
            Offers.save_offer_images(db, offer_id, configuration.offer_root_dir, files)
        else:
            raise HTTPException(status_code=400, detail="At least one file is not an image")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


@router.delete("/{offer_id}/images/{image_name}")
def delete_offer_image(offer_id: int, image_name: str, db: Session = Depends(setup_database.get_db)):
    try:
        Offers.delete_offer_image(db, offer_id, image_name, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=f"File {e.filename} not found")
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)


# As of the current fastapi version, the ResponseModel Parameter does not work with a FileResponse class
# This might be fixed in a future version and should only affect the documentation
@router.get("/{offer_id}/thumbnail")
def get_offer_thumbnail(offer_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        image_path = Offers.get_thumbnail_path(db, offer_id, configuration.offer_root_dir)
        return FileResponse(image_path)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=f"File {e.filename} not found")
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)

