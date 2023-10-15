from API import setup_database
from API.Crud import Categories
from API.Schemas import Category
from API.Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import exc

from API.Utils.Exceptions import EntryNotFoundException

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post("/", response_model=Category.Category, status_code=status.HTTP_201_CREATED)
def add_category(category: Category.CategoryCreate, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.create_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.put("/", response_model=Category.Category)
def update_category(category: Category.Category, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.update_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/")
def delete_category(category_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        Categories.delete_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{category_id}", response_model=Category.Category)
def get_category(category_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Category.Category])
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


@router.get("/{category_id}/offers", response_model=Relations.CategoryWithOffers)
def get_category_with_offers(category_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{category_id}/subcategories", response_model=Relations.CategoryWithSubcategories)
def get_category_with_subcategories(category_id: int, db: Session = Depends(setup_database.get_db)):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
