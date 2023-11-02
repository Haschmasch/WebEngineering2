"""
Contains all API endpoints for the '/followings' route.
"""


import setup_database
from Crud import Followings
from Schemas import Following
from Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy import exc
from Utils.Exceptions import EntryNotFoundException
from Schemas.User import User
from Utils.Authentication import decode_and_validate_token
from typing import Annotated


router = APIRouter(
    prefix="/followings",
    tags=["followings"]
)


@router.post("/", response_model=Following.Following, status_code=status.HTTP_201_CREATED)
def add_following(following: Following.FollowingCreate,
                  current_user: Annotated[User, Depends(decode_and_validate_token)],
                  db: Session = Depends(setup_database.get_db)):
    """
    Adds the provided following to the database. Only authenticated users can use this endpoint.
    Trying to create a following that belongs to another user than the authenticated user raises an error.
    :param following: The offer to be created.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code with a following model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        if following.user_id == current_user.id:
            return Followings.create_following(db, following)
        raise HTTPException(status_code=400,
                            detail="Adding a following for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_following(following_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                     db: Session = Depends(setup_database.get_db)):
    """
    Deletes the provided following by the following id from the database.
    Only authenticated users can use this endpoint.
    Trying to delete a following that belongs to another user than the authenticated user raises an error.
    :param following_id: The following id for the category to be deleted.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 204 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the following was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        following = Followings.get_following(db, following_id)
        if following.user_id == current_user.id:
            Followings.delete_following(db, following_id)
        else:
            raise HTTPException(status_code=400,
                                detail="Deleting a following for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{following_id}", response_model=Relations.FollowingWithOffer)
def get_following(following_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided following with the related offer by the following id from the database.
    :param following_id: The following id for the following.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a following model and the related offer be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the following was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Followings.get_following(db, following_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Relations.FollowingWithOffer])
def get_followings(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    """
    Gets all followings with their related offer from the database limited by skip and limit attributes.
    :param skip: The starting number of followings. All followings before this number will be skipped.
    :param limit: The last following to be included. Any followings after the limit will not be included.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a list of following models and their related offers
    will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the following was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Followings.get_followings(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/user/{user_id}", response_model=list[Relations.FollowingWithOffer])
def get_followings_by_user(user_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets all followings with their related offer from the database by the user that is associated with them.
    :param user_id: The id of the user.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a list of following models and their related offers
    will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the following was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Followings.get_followings_by_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
