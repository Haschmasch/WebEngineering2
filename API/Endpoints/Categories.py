from API import setup_database
from API.Crud import Categories
from API.Schemas import Category
from API.Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import exc
from API.Schemas.User import User
from API.Utils.Authentication import decode_and_validate_token
from typing import Annotated

from API.Utils.Exceptions import EntryNotFoundException

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post("/", response_model=Category.Category, status_code=status.HTTP_201_CREATED)
def add_category(category: Category.CategoryCreate, current_user: Annotated[User, Depends(decode_and_validate_token)],
                 db: Session = Depends(setup_database.get_db)):
    # TODO: Validate user group
    try:
        return Categories.create_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)


@router.put("/", response_model=Category.Category)
def update_category(category: Category.Category, current_user: Annotated[User, Depends(decode_and_validate_token)],
                    db: Session = Depends(setup_database.get_db)):
    # TODO: Validate user group
    try:
        return Categories.update_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                    db: Session = Depends(setup_database.get_db)):
    try:
        # TODO: Validate user group
        Categories.delete_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{category_id}", response_model=Relations.CategoryWithSubcategories)
def get_category(category_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Relations.CategoryWithSubcategories])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.get_categories(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/name/{category_name}", response_model=Category.Category)
def get_category_by_name(category_name: str, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.get_category_by_name(db, category_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offers/{category_id}", response_model=Relations.CategoryWithOffers)
def get_category_with_offers(category_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
