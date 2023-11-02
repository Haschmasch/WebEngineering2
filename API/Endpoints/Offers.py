"""
Contains all API endpoints for the '/offers' route.
"""

import setup_database
from Crud import Offers
from Schemas import Offer
from Schemas import Relations
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status, UploadFile, APIRouter
from sqlalchemy import exc
from Utils.ConfigManager import configuration
from fastapi.responses import Response, FileResponse
from Utils.Exceptions import EntryNotFoundException
from Schemas.User import User
from Utils.Authentication import decode_and_validate_token
from typing import Annotated


router = APIRouter(
    prefix="/offers",
    tags=["offers"]
)


@router.post("/", response_model=Relations.OfferWithRelations, status_code=status.HTTP_201_CREATED)
def add_offer(offer: Offer.OfferCreate, current_user: Annotated[User, Depends(decode_and_validate_token)],
              db: Session = Depends(setup_database.get_db)):
    """
    Adds the provided offer to the database. Only authenticated users can use this endpoint.
    Trying to create an offer that belongs to another user than the authenticated user raises an error.
    :param offer: The offer to be created.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code with an offer model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        if offer.user_id == current_user.id:
            return Offers.create_offer(db, offer, configuration.offer_root_dir)
        raise HTTPException(status_code=400,
                            detail="Creating a offer for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.put("/", response_model=Relations.OfferWithRelations)
def update_offer(offer: Offer.Offer, current_user: Annotated[User, Depends(decode_and_validate_token)],
                 db: Session = Depends(setup_database.get_db)):
    """
    Updates the provided offer in the database. Only authenticated users can use this endpoint.
    Trying to update an offer that belongs to another user than the authenticated user raises an error.
    :param offer: The offer to be updated.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with an offer model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If a user model that does not match the authenticated user is provided,
     a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        if offer.user_id == current_user.id:
            return Offers.update_offer(db, offer, configuration.offer_root_dir)
        raise HTTPException(status_code=400,
                            detail="Updating a offer for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer(offer_id: int, current_user: Annotated[User, Depends(decode_and_validate_token)],
                 db: Session = Depends(setup_database.get_db)):
    """
    Deletes the provided offer by the offer id from the database. This also deleted all related files from the folder
    structure of the offer. Only authenticated users can use this endpoint.
    Trying to delete an offer that belongs to another user than the authenticated user raises an error.
    :param offer_id: The offer id for the offer to be deleted.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 204 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If a user model that does not match the authenticated user is provided,
    a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        offer = Offers.get_offer(db, offer_id)
        if offer.user_id == current_user.id:
            Offers.delete_offer(db, offer_id, configuration.offer_root_dir)
        else:
            raise HTTPException(status_code=400,
                                detail="Updating a offer for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{offer_id}", response_model=Relations.OfferWithRelations)
def get_offer(offer_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets the provided offer by the user id from the database.
    :param offer_id: The user id for the user.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with an offer model will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Offers.get_offer(db, offer_id)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/", response_model=list[Relations.OfferWithRelations])
def get_offers(skip: int = 0, limit: int = 100, db: Session = Depends(setup_database.get_db)):
    """
    Gets all offers from the database limited by skip and limit attributes.
    :param skip: The starting number of offers. All offers before this number will be skipped.
    :param limit: The last offer to be included. Any offers after the limit will not be included.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a list of offer models will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Offers.get_offers(db, skip, limit)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.strerror)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{offer_id}/images", response_class=Response)
def get_offer_images(offer_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets all images associated with an offer by the id compressed as a zip-file.
    :param offer_id: The id of the offer.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a zip file  will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Offers.get_offer_images(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{offer_id}/images/names")
def get_offer_images(offer_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets all image names associated with an offer by the id as a list of strings.
    :param offer_id: The id of the offer.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with a zip file  will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        return Offers.get_offer_image_names(db, offer_id, configuration.offer_root_dir)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/{offer_id}/images/{image_name}")
def get_offer_image(offer_id: int, image_name: str, db: Session = Depends(setup_database.get_db)):
    """
    Gets an image from an offer based on their id and name.
    :param offer_id: The offer id for the image path.
    :param image_name: The individual image name.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 200 status code with an image will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        image_path = Offers.get_image_path(db, offer_id, image_name, configuration.offer_root_dir)
        return FileResponse(image_path)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/{offer_id}/images", status_code=status.HTTP_201_CREATED)
def create_offer_images(offer_id: int, files: list[UploadFile],
                        current_user: Annotated[User, Depends(decode_and_validate_token)],
                        db: Session = Depends(setup_database.get_db)):
    """
    Upload images as multipart/form-data. The images are then stored in a directory related to the offer.
    Only authenticated users can use this endpoint. Trying to upload images
    that belong to another user than the authenticated user raises an error.
    :param offer_id: The offer id for the image path.
    :param files: The individual image name.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If an uploaded file is not an image, a 400 status code with an error message will be returned.
    If an offer id that does not match the authenticated user is provided,
    a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        offer = Offers.get_offer(db, offer_id)
        if offer.user_id == current_user.id:
            if all("image" in file.content_type for file in files):
                Offers.save_offer_images(db, offer_id, configuration.offer_root_dir, files)
            else:
                raise HTTPException(status_code=400, detail="At least one file is not an image")
        else:
            raise HTTPException(status_code=400,
                                detail="Creating offer images for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/{offer_id}/images/{image_name}")
def delete_offer_image(offer_id: int, image_name: str,
                       current_user: Annotated[User, Depends(decode_and_validate_token)],
                       db: Session = Depends(setup_database.get_db)):
    """
    Deletes a specified image from an offer. Only authenticated users can use this endpoint. Trying to delete images
    that belong to another user than the authenticated user raises an error.
    :param offer_id: The offer id for the image path.
    :param image_name: The individual image name.
    :param current_user: The current user. Acquired by decoding the jwt token.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If an offer id that does not match the authenticated user is provided,
    a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        offer = Offers.get_offer(db, offer_id)
        if offer.user_id == current_user.id:
            Offers.delete_offer_image(db, offer_id, image_name, configuration.offer_root_dir)
        else:
            raise HTTPException(status_code=400,
                                detail="Deleting an offer image for a user who is not authenticated is not allowed")
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)


# As of the current fastapi version, the ResponseModel Parameter does not work with a FileResponse class
# This might be fixed in a future version and should only affect the documentation
@router.get("/{offer_id}/thumbnail")
def get_offer_thumbnail(offer_id: int, db: Session = Depends(setup_database.get_db)):
    """
    Gets the thumbnail image from an offer.
    :param offer_id: The offer id for the image path.
    :param db: The database object, that is supplied via dependency injection.
    :return: If successful, a 201 status code will be returned.
    If a database error occurred, a 400 status code with an error message will be returned.
    If the offer was not found, a 404 status code with an error message will be returned.
    An internal server error (500) is returned, when an unhandled exception is raised.
    """
    try:
        image_path = Offers.get_thumbnail_path(db, offer_id, configuration.offer_root_dir)
        return FileResponse(image_path)
    except exc.DatabaseError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)
    except OSError as os_error:
        raise HTTPException(status_code=400, detail=os_error.args)
    except EntryNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.args)
