"""
Contains all create, read, update and delete operations for offers.
This file also contains directory operations for saving images
"""

import datetime
from Utils.Exceptions import EntryNotFoundException
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from fastapi import UploadFile
import models
from Utils import FileOperations
from Schemas import Offer
import os
import zipfile
import io
from fastapi.responses import Response


def create_offer(db: Session, offer: Offer.OfferCreate, offer_root_directory: str):
    offer.short_description = get_short_description(offer.description)
    db_offer = models.Offer(title=offer.title,
                            category_id=offer.category_id,
                            subcategory_id=offer.subcategory_id,
                            price=offer.price,
                            currency=offer.currency,
                            user_id=offer.user_id,
                            time_posted=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
                            postcode=offer.postcode,
                            city=offer.city,
                            address=offer.address,
                            primary_image=offer.primary_image,
                            short_description=offer.short_description,
                            description=offer.description)
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    image_path = get_image_directory(offer_root_directory, db_offer.user_id, db_offer.id)
    FileOperations.create_thumbnail(f"{image_path}/{db_offer.primary_image}")
    return db_offer


def delete_offer(db: Session, offer_id: int, offer_root_directory: str):
    offer = get_offer(db, offer_id)
    if offer is not None:
        db.execute(delete(models.Offer).where(models.Offer.id == offer_id))
        db.commit()
        FileOperations.remove_directory(f"{offer_root_directory}/{offer.user_id}/{offer.id}")
    else:
        raise EntryNotFoundException(f"No database entry found for offer_id: {offer_id}")


# This is inefficient, because the whole offer is updated, even if only a single value changes
# This can also lead to the removal of values in the database, if an empty value is set here
def update_offer(db: Session, offer: Offer.Offer, offer_root_directory: str):
    offer.short_description = get_short_description(offer.description)
    if offer.closed and offer.time_closed is None:
        offer.time_closed = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    if not offer.closed:
        offer.time_closed = None
    result = db.scalars(update(models.Offer)
                        .returning(models.Offer)
                        .where(models.Offer.id == offer.id)
                        .values(title=offer.title,
                                category_id=offer.category_id,
                                subcategory_id=offer.subcategory_id,
                                price=offer.price,
                                currency=offer.currency,
                                postcode=offer.postcode,
                                city=offer.city,
                                address=offer.address,
                                closed=offer.closed,
                                time_closed=offer.time_closed,
                                primary_image=offer.primary_image,
                                short_description=offer.short_description,
                                description=offer.description))
    # Note, that the userid and time posted fields are purposefully not overwritten here,
    # since they only receive an initial value.
    db.commit()
    image_path = get_image_directory(offer_root_directory, offer.user_id, offer.id)
    FileOperations.create_thumbnail(f"{image_path}/{offer.primary_image}")
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for offer: {offer.id}")


def get_offer(db: Session, offer_id: int):
    result = db.scalars(select(models.Offer)
                        .where(models.Offer.id == offer_id))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for offer_id: {offer_id}")


def get_offers(db: Session, first: int, last: int):
    result = db.scalars(select(models.Offer)
                        .offset(first).limit(last))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for first: {first}, last: {last}")


def save_offer_images(db: Session, offer_id: int, offer_root_directory: str, files: list[UploadFile]):
    offer = get_offer(db, offer_id)
    path = get_image_directory(offer_root_directory, offer.user_id, offer_id)
    for file in files:
        FileOperations.write_uploaded_file(f"{path}/{file.filename}", file)
    FileOperations.create_thumbnail(f"{path}/{offer.primary_image}")


def get_offer_images(db: Session, offer_id: int, offer_root_directory: str):
    # See: https://stackoverflow.com/questions/61163024/return-multiple-files-from-fastapi for more info
    offer = get_offer(db, offer_id)
    zip_filename = f"{offer.id}_images.zip"
    path = get_image_directory(offer_root_directory, offer.user_id, offer_id)
    path = FileOperations.try_resolve_relative_path(path)
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in FileOperations.get_file_paths(path):
        # Calculate path for file in zip
        filedir, filename = os.path.split(fpath)

        # Add file, at correct path
        zf.write(fpath, filename)
    # Must close zip for all contents to be written
    zf.close()
    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })
    return resp


def get_offer_image_names(db: Session, offer_id: int, offer_root_directory: str):
    offer = get_offer(db, offer_id)
    path = get_image_directory(offer_root_directory, offer.user_id, offer_id)
    return FileOperations.get_file_names(path)


def get_image_path(db: Session, offer_id: int, image_name: str, offer_root_directory: str):
    offer = get_offer(db, offer_id)
    path = get_image_directory(offer_root_directory, offer.user_id, offer_id)
    return f"{path}/{image_name}"


def get_thumbnail_path(db: Session, offer_id: int, offer_root_directory: str):
    offer = get_offer(db, offer_id)
    path = get_image_directory(offer_root_directory, offer.user_id, offer_id)
    return FileOperations.get_thumbnail_path(f"{path}/{offer.primary_image}")


def delete_offer_image(db: Session, offer_id: int, image_name: str, offer_root_directory: str):
    path = get_image_path(db, offer_id, image_name, offer_root_directory)
    FileOperations.remove_file(path)


def get_image_directory(offer_root_directory, user_id, offer_id):
    return f"{offer_root_directory}/{user_id}/{offer_id}/images"


def get_short_description(description: str):
    short_description = description
    if len(short_description) > 50:
        short_description = description[0:49]
        last_blank = short_description.rfind(' ')
        while last_blank > 46:
            last_blank = short_description.rfind(' ', 0, last_blank)
        short_description = description[0:last_blank]
    return short_description
