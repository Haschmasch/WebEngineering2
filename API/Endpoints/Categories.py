from API import setup_database
from API.Crud import Categories
from API.Schemas import Category
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import exc
from API.setup_api import app


@app.post("/categories/", response_model=Category.Category, status_code=status.HTTP_201_CREATED)
def add_category(category: Category.CategoryCreate, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.create_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.put("/categories/", response_model=Category.Category)
def update_user(category: Category.Category, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.update_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.delete("/categories/", response_model=Category.Category)
def delete_category(category_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.delete_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/categories/{category_id}", response_model=Category.Category)
def get_user(category_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/categories/name/{category_name}", response_model=Category.Category)
def get_user_by_name(category_name: str, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.get_category_by_name(db, category_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


# TODO: Integrate relations for offers
@app.get("/categories/{category_id}/offers", response_model=Category.CategoryWithOffers)
def get_category_with_offers(category_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/categories/{category_id}/subcategories", response_model=Category.CategoryWithSubcategories)
def get_category_with_offers(category_id: int, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@app.get("/categories/", response_model=list[Category.Category])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db())):
    try:
        return Categories.get_categories(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.detail)


