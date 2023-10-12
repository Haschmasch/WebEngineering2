from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from fastapi import UploadFile
from API import models
from API.Utils import FileOperations
from API.Schemas import Offer
import os
import zipfile
import io
from fastapi.responses import Response


def create_offer(db: Session, offer: Offer.OfferCreate, offer_root_directory: str):
    result = db.execute(insert(models.Offer).values(title=offer.title,
                                                    categoryid=offer.category_id,
                                                    subcategoryid=offer.subcategory_id,
                                                    price=offer.price,
                                                    currency=offer.currency,
                                                    userid=offer.userid,
                                                    timeposted=offer.time_posted,
                                                    postcode=offer.postcode,
                                                    city=offer.city,
                                                    address=offer.address,
                                                    primaryimage=offer.primary_image))
    db.commit()
    primary_key = result.inserted_primary_key[0]
    path = get_description_path(offer_root_directory, offer.userid, primary_key)
    FileOperations.write_text_file(path, offer.description)
    return result.first()


def save_offer_images(db: Session, offer_root_directory: str, offer_id: int, files: list[UploadFile]):
    offer = get_offer(db, offer_id, offer_root_directory)
    path = get_image_directory(offer_root_directory, offer.userid, offer_id)
    for file in files:
        FileOperations.write_uploaded_file(f"{path}/{file.filename}", file)


def get_offer_images(db: Session, offer_id: int, offer_root_directory: str):
    # See: https://stackoverflow.com/questions/61163024/return-multiple-files-from-fastapi for more info
    offer = get_offer(db, offer_id, offer_root_directory)
    zip_filename = f"{offer.id}_images.zip"
    path = get_image_directory(offer_root_directory, offer.userid, offer_id)

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


def delete_offer(db: Session, offer_id: int, offer_root_directory: str):
    offer = get_offer(db, offer_id, offer_root_directory)
    result = db.execute(delete(models.Offer).where(models.Offer.id == offer_id))
    db.commit()
    FileOperations.remove_directory(f"{offer_root_directory}/{offer.userid}/{offer.id}")
    return result.first()


# This is inefficient, because the whole offer is updated, even if only a single value changes
# This can also lead to the removal of values in the database, if an empty value is set here
def update_offer(db: Session, offer: Offer.Offer, offer_root_directory: str):
    result = db.execute(update(models.Offer)
                        .where(models.Offer.id == offer.id)
                        .values(title=offer.title,
                                category_id=offer.category_id,
                                subcategory_id=offer.subcategory_id,
                                price=offer.price,
                                currency=offer.price,
                                postcode=offer.postcode,
                                city=offer.city,
                                address=offer.address,
                                closed=offer.closed,
                                timeclosed=offer.time_closed,
                                primaryimage=offer.primary_image))
    # Note, that the userid and timeposted fields are purposefully not overwritten here,
    # since they only receive an initial value.
    db.commit()
    path = get_description_path(offer_root_directory, offer.userid, offer.id)
    FileOperations.write_text_file(path, offer.description)
    return result.first()


# TODO: Add description to returned offers.
def get_offer(db: Session, offer_id: int, offer_root_directory: str):
    result = db.execute(select(models.Offer)
                        .join(models.Offer.category)
                        .join(models.Offer.subcategory)
                        .where(models.Offer.id == offer_id))
    offer = result.first()
    offer.description = FileOperations.read_text_file(
        get_description_path(offer_root_directory, offer.userid, offer.id))
    return offer


def get_offers(db: Session, first: int, last: int, offer_root_directory: str):
    result = db.execute(select(models.Offer)
                        .join(models.Offer.category)
                        .join(models.Offer.subcategory)
                        .offset(first).limit(last))
    return add_description_to_results(result, offer_root_directory)


def get_offers_by_user(db: Session, user_id: int, offer_root_directory: str):
    result = db.execute(select(models.Offer)
                        .join(models.Offer.category)
                        .join(models.Offer.subcategory)
                        .where(models.Offer.userid == user_id))
    return add_description_to_results(result, offer_root_directory)


def get_offers_by_category(db: Session, category_id: int, offer_root_directory: str):
    result = db.execute(select(models.Offer)
                        .join(models.Offer.category)
                        .join(models.Offer.subcategory)
                        .where(models.Offer.categoryid == category_id))
    return add_description_to_results(result, offer_root_directory)


def get_offers_by_subcategory(db: Session, subcategory_id: int, offer_root_directory: str):
    result = db.execute(select(models.Offer)
                        .join(models.Offer.category)
                        .join(models.Offer.subcategory)
                        .where(models.Offer.subcategoryid == subcategory_id))
    return add_description_to_results(result, offer_root_directory)


def add_description_to_results(result, offer_root_directory: str):
    results = result.all()
    for offer in result:
        offer.description = FileOperations.read_text_file(
            get_description_path(offer_root_directory, offer.userid, offer.id))
    return results


def get_description_path(offer_root_directory, user_id, offer_id):
    return f"{offer_root_directory}/{user_id}/{offer_id}/description.txt"


def get_image_directory(offer_root_directory, user_id, offer_id):
    return f"{offer_root_directory}/{user_id}/{offer_id}/images"
