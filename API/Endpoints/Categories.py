"""
Contains all API endpoints for the '/categories' route.
"""

import setup_database
from Crud import Categories
from Schemas import Category
from Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy import exc
from Schemas.User import User
from Utils.Authentication import decode_and_validate_token
from typing import Annotated
from Utils.Exceptions import EntryNotFoundException


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post("/", response_model=Category.Category, status_code=status.HTTP_201_CREATED)
def add_category(category: Category.CategoryCreate, current_user: Annotated[User, Depends(decode_and_validate_token)],
                 db: Session = Depends(setup_database.get_db)):
    """
    Adds the provided category to the database. Only authenticated users can use this endpoint.
    :param category: The category to be created.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code with a category model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Categories.create_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)


@router.put("/", response_model=Category.Category)
def update_category(category: Category.Category, current_user: Annotated[User, Depends(decode_and_validate_token)],
                    db: Session = Depends(setup_database.get_db)):
    """
    Updates the provided category in the database. Only authenticated users can use this endpoint.
    :param category: The category to be updated.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a category model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Categories.update_category(db, category)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                    db: Session = Depends(setup_database.get_db)):
    """
    Deletes the provided category by the category_id from the database. Only authenticated users can use this endpoint.
    :param category_id: The category id for the category to be deleted.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 204 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        Categories.delete_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{category_id}", response_model=Relations.CategoryWithSubcategories)
def get_category(category_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided category with all related subcategories by the category id from the database.
    :param category_id: The category id for the category.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a category model and all related subcategories be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Relations.CategoryWithSubcategories])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    """
    Gets all categories with all related subcategories from the database limited by skip and limit attributes.
    :param skip: The starting number of categories. All categories before this number will be skipped.
    :param limit: The last category to be included. Any categories after the limit will not be included.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a list of category models and all related subcategories
    will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Categories.get_categories(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/name/{category_name}", response_model=Category.Category)
def get_category_by_name(category_name: str, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided category by the category name from the database.
    :param category_name: The category name for the category.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a category model be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Categories.get_category_by_name(db, category_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offers/{category_id}", response_model=Relations.CategoryWithOffers)
def get_category_with_offers(category_id: int, db: Session = Depends(setup_database.get_db)):
    """
     Gets the provided category by the category id from the database.
     This also includes a list of all offers with the same category id
     :param category_id: The category id for the category.
     :param db: The database object, that is supplied via dependency injection.
     :return: If successful, a 200 status code with a category model and the underlying offers
     will be returned.
     If a database error occurred, a 400 status code with an error message will be returned.
     If the category was not found, a 404 status code with an error message will be returned.
     An internal server error (500) is returned, when an unhandled exception is raised.
     """
    try:
        return Categories.get_category(db, category_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
