"""
Contains all API endpoints for the '/users' route.
"""

from datetime import timedelta
from API import setup_database
from API.Crud import Users
from API.Schemas import JwtTokenData
from API.Schemas.User import User, UserCreate
from API.Schemas import Relations
from API.Utils.Authentication import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_and_validate_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exc
from typing import Annotated

from API.Utils.Exceptions import EntryNotFoundException

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(setup_database.get_db)):
    """
    Adds the provided user to the database.
    :param user: The user to be created.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code with a user model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Users.create_user(db, user)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)


# TODO: Implement proper login (maybe with jwt tokens)
@router.post("/login", response_model=JwtTokenData.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: Session = Depends(setup_database.get_db)):
    """
    This is the login function for users. It returns a jwt bearer token.
    :param form_data: The user credentials are passed as form data using the OAuth2 specification, not as a json object.
    :param db: The database object, that is supplied via dependency injection.
    :return: The JWT bearer token.
    """
    user = Users.check_user_exists(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/", response_model=User)
def update_user(user: User, current_user: Annotated[User, Depends(decode_and_validate_token)],
                db: Session = Depends(setup_database.get_db)):
    """
    Updates the provided user in the database. Only authenticated users can use this endpoint.
    Trying to update a user aside from the authenticated user raises an error.
    :param user: The user to be updated.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a category model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If a user model that does not match the authenticated user is provided,
     a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        if user.id == current_user.id:
            return Users.update_user(db, user)
        raise HTTPException(status_code=400, detail="Updating a user aside from the authenticated user is not allowed.")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(user_id: int, user: UserCreate,
                         current_user: Annotated[User, Depends(decode_and_validate_token)],
                         db: Session = Depends(setup_database.get_db)):
    """
    Updates the provided user password in the database. Only authenticated users can use this endpoint.
    Trying to update a user password aside from the authenticated user raises an error.
    :param user_id: The id of the user to be updated.
    :param user: The user model with the password.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a category model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If a user model that does not match the authenticated user is provided,
     a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        if user_id == current_user.id:
            return Users.update_user_password(db, user_id, user)
        raise HTTPException(status_code=400, detail="Updating a user aside from the authenticated user is not allowed.")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                db: Session = Depends(setup_database.get_db)):
    """
    Deletes the provided user by the user id from the database. Only authenticated users can use this endpoint.
    Trying to delete a user aside from the authenticated user raises an error.
    :param user_id: The category id for the category to be deleted.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 204 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If a user model that does not match the authenticated user is provided,
    a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        if user_id == current_user.id:
            Users.delete_user(db, user_id)
        else:
            raise HTTPException(status_code=400,
                                detail="Deleting a user aside from the authenticated user is not allowed.")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided user by the user id from the database.
    :param user_id: The user id for the user.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a user model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Users.get_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    """
    Gets all users from the database limited by skip and limit attributes.
    :param skip: The starting number of users. All users before this number will be skipped.
    :param limit: The last user to be included. Any users after the limit will not be included.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a list of user models will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Users.get_users(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/current", response_model=User)
def get_user(current_user: Annotated[User, Depends(decode_and_validate_token)]):
    """
    Gets the user from the current JWT token.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :return: If successful, a 200 status code with a user model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return current_user
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/name/{user_name}", response_model=User)
def get_user_by_name(user_name: str, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided user by the username from the database.
    :param user_name: The username for the category.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a user model be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the category was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Users.get_user_by_name(db, user_name)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/offers/{user_id}/", response_model=Relations.UserWithOffers)
def get_user_with_offers(user_id: int, db: Session = Depends(setup_database.get_db)):
    """
     Gets the provided user by the user id from the database.
     This also includes a list of all offers with the same user id
     :param user_id: The user id for the category.
     :param db: The database object, that is supplied via dependency injection.
     :return: If successful, a 200 status code with a user model and the underlying offers
     will be returned.
     If a database error occurred, a 400 status code with an error message will be returned.
     If the category was not found, a 404 status code with an error message will be returned.
     An internal server error (500) is returned, when an unhandled exception is raised.
     """
    try:
        return Users.get_user(db, user_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
