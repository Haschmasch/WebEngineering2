from API import setup_database
from API.Crud import Subcategories
from API.Schemas import Subcategory
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import exc
from API.setup_api import app


@app.post("/subcategories/", response_model=Subcategory.Subcategory, status_code=status.HTTP_201_CREATED)
def add_category(subcategory: Subcategory.SubcategoryCreate, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.create_subcategory(db, subcategory)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.put("/subcategories/", response_model=Subcategory.Subcategory)
def update_user(subcategory: Subcategory.Subcategory, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.update_subcategory(db, subcategory)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.delete("/subcategories/", response_model=Subcategory.Subcategory)
def delete_category(subcategory_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.delete_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/subcategories/{subcategory_id}", response_model=Subcategory.Subcategory)
def get_user(subcategory_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/subcategories/name/{subcategory_name}", response_model=Subcategory.Subcategory)
def get_user_by_name(subcategory_name: str, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.get_subcategory_by_name(db, subcategory_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


# TODO: Integrate relations for offers
@app.get("/subcategories/{subcategory_id}/offers", response_model=Subcategory.SubcategoryWithOffers)
def get_category_with_offers(subcategory_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/subcategories/{subcategory_id}/category", response_model=Subcategory.SubcategoryWithCategory)
def get_category_with_offers(subcategory_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/subcategories/", response_model=list[Subcategory.Subcategory])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db())):
    try:
        return Subcategories.get_subcategories(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


