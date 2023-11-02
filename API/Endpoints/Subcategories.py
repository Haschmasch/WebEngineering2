"""
Contains all API endpoints for the '/subcategories' route.
"""

import setup_database
from Crud import Subcategories
from Schemas import Subcategory
from Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy import exc
from Utils.Exceptions import EntryNotFoundException
from Schemas.User import User
from Utils.Authentication import decode_and_validate_token
from typing import Annotated


router = APIRouter(
    prefix="/subcategories",
    tags=["subcategories"]
)


@router.post("/", response_model=Subcategory.Subcategory, status_code=status.HTTP_201_CREATED)
def add_subcategory(subcategory: Subcategory.SubcategoryCreate,
                    current_user: Annotated[User, Depends(decode_and_validate_token)],
                    db: Session = Depends(setup_database.get_db)):
    """
    Adds the provided subcategory to the database. Only authenticated users can use this endpoint.
    :param subcategory: The subcategory to be created.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code with a subcategory model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Subcategories.create_subcategory(db, subcategory)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.put("/", response_model=Subcategory.Subcategory)
def update_subcategory(subcategory: Subcategory.Subcategory,
                       current_user: Annotated[User, Depends(decode_and_validate_token)],
                       db: Session = Depends(setup_database.get_db)):
    """
    Updates the provided subcategory in the database. Only authenticated users can use this endpoint.
    :param subcategory: The subcategory to be updated.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a subcategory model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Subcategories.update_subcategory(db, subcategory)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(subcategory_id: int,
                       current_user: Annotated[User, Depends(decode_and_validate_token)],
                       db: Session = Depends(setup_database.get_db)):
    """
    Deletes the provided subcategory by the subcategory_id from the database.
    Only authenticated users can use this endpoint.
    :param subcategory_id: The subcategory id for the subcategory to be deleted.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 204 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        Subcategories.delete_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{subcategory_id}", response_model=Subcategory.Subcategory)
def get_subcategory(subcategory_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided subcategory by the subcategory id from the database.
    :param subcategory_id: The subcategory id for the category.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a subcategory model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Subcategory.Subcategory])
def get_subcategories(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    """
    Gets all categories from the subcategory limited by skip and limit attributes.
    :param skip: The starting number of offers. All offers before this number will be skipped.
    :param limit: The last offer to be included. Any offers after the limit will not be included.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a list of subcategory models will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Subcategories.get_subcategories(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/name/{subcategory_name}", response_model=Subcategory.Subcategory)
def get_subcategory_by_name(subcategory_name: str, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided subcategory by the category name from the database.
    :param subcategory_name: The subcategory name for the category.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a subcategory model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Subcategories.get_subcategory_by_name(db, subcategory_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offers/{subcategory_id}/", response_model=Relations.SubcategoryWithOffers)
def get_subcategory_with_offers(subcategory_id: int, db: Session = Depends(setup_database.get_db)):
    """
     Gets the provided subcategory by the subcategory id from the database.
     This also includes a list of all offers with the same category id
     :param subcategory_id: The category id for the category.
     :param db: The database object, that is supplied via dependency injection.
     :return: If successful, a 200 status code with a subcategory model and the underlying offers
       will be returned.
     If a database error occurred, a 400 status code with an error message will be returned.
     If the category was not found, a 404 status code with an error message will be returned.
     An internal server error (500) is returned, when an unhandled exception is raised.
     """
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/category/{subcategory_id}/", response_model=Relations.SubcategoryWithCategory)
def get_subcategory_with_category(subcategory_id: int, db: Session = Depends(setup_database.get_db)):
    """
     Gets the provided subcategory by the subcategory id from the database.
     This also includes the parent category of the subcategory.
     :param subcategory_id: The category id for the category.
     :param db: The database object, that is supplied via dependency injection.
     :return: If successful, a 200 status code with a subcategory model and the underlying category
       will be returned.
     If a database error occurred, a 400 status code with an error message will be returned.
     If the category was not found, a 404 status code with an error message will be returned.
     An internal server error (500) is returned, when an unhandled exception is raised.
     """
    try:
        return Subcategories.get_subcategory(db, subcategory_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
