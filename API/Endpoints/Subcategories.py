from API import setup_database
from API.Crud import Subcategories
from API.Schemas import Subcategory
from API.Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import exc

from API.Utils.Exceptions import EntryNotFoundException

router = APIRouter(
    prefix="/subcategories",
    tags=["subcategories"]
)


@router.post("/", response_model=Subcategory.Subcategory, status_code=status.HTTP_201_CREATED)
def add_subcategory(subcategory: Subcategory.SubcategoryCreate, db: Session = Depends(setup_database.get_db)):
    try:
        return Subcategories.create_subcategory(db, subcategory)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.put("/", response_model=Subcategory.Subcategory)
def update_subcategory(subcategory: Subcategory.Subcategory, db: Session = Depends(setup_database.get_db)):
    try:
        return Subcategories.update_subcategory(db, subcategory)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(subcategory_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        Subcategories.delete_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{subcategory_id}", response_model=Subcategory.Subcategory)
def get_subcategory(subcategory_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Subcategory.Subcategory])
def get_subcategories(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Subcategories.get_subcategories(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/name/{subcategory_name}", response_model=Subcategory.Subcategory)
def get_subcategory_by_name(subcategory_name: str, db: Session = Depends(setup_database.get_db)):
    try:
        return Subcategories.get_subcategory_by_name(db, subcategory_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offers/{subcategory_id}/", response_model=Relations.SubcategoryWithOffers)
def get_subcategory_with_offers(subcategory_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("category/{subcategory_id}/", response_model=Relations.SubcategoryWithCategory)
def get_subcategory_with_category(subcategory_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
