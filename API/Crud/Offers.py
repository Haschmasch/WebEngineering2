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
    offer.short_description = get_short_description(offer.description)
    db_offer = models.Offer(title=offer.title,
                            categoryid=offer.category_id,
                            subcategoryid=offer.subcategory_id,
                            price=offer.price,
                            currency=offer.currency,
                            userid=offer.user_id,
                            timeposted=offer.time_posted,
                            postcode=offer.postcode,
                            city=offer.city,
                            address=offer.address,
                            primaryimage=offer.primary_image,
                            shortdescription=offer.short_description)
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    desc_path = get_description_path(offer_root_directory, db_offer.userid, db_offer.id)
    image_path = get_image_directory(offer_root_directory, db_offer.userid, db_offer.id)
    FileOperations.create_thumbnail(f"{image_path}/{db_offer.primaryimage}")
    FileOperations.write_text_file(desc_path, offer.description)
    return db_offer


def delete_offer(db: Session, offer_id: int, offer_root_directory: str):
    offer = get_offer(db, offer_id, offer_root_directory)
    db.execute(delete(models.Offer).where(models.Offer.id == offer_id))
    db.commit()
    FileOperations.remove_directory(f"{offer_root_directory}/{offer.userid}/{offer.id}")


# This is inefficient, because the whole offer is updated, even if only a single value changes
# This can also lead to the removal of values in the database, if an empty value is set here
def update_offer(db: Session, offer: Offer.Offer, offer_root_directory: str):
    offer.short_description = get_short_description(offer.description)
    result = db.scalars(update(models.Offer)
                        .returning(models.Offer)
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
                                primaryimage=offer.primary_image,
                                shortdescription=offer.short_description))
    # Note, that the userid and timeposted fields are purposefully not overwritten here,
    # since they only receive an initial value.
    db.commit()
    path = get_description_path(offer_root_directory, offer.user_id, offer.id)
    image_path = get_image_directory(offer_root_directory, offer.user_id, offer.id)
    FileOperations.create_thumbnail(f"{image_path}/{offer.primary_image}")
    FileOperations.write_text_file(path, offer.description)
    return result.first()


def get_offer(db: Session, offer_id: int, offer_root_directory: str):
    result = db.scalars(select(models.Offer)
                        .where(models.Offer.id == offer_id))
    offer = result.first()
    offer.description = FileOperations.read_text_file(
        get_description_path(offer_root_directory, offer.userid, offer.id))
    return offer


def get_offers(db: Session, first: int, last: int, offer_root_directory: str):
    result = db.scalars(select(models.Offer)
                        .offset(first).limit(last))
    return add_description_to_results(result.all(), offer_root_directory)


def save_offer_images(db: Session, offer_id: int, offer_root_directory: str, files: list[UploadFile]):
    offer = get_offer(db, offer_id, offer_root_directory)
    path = get_image_directory(offer_root_directory, offer.userid, offer_id)
    for file in files:
        FileOperations.write_uploaded_file(f"{path}/{file.filename}", file)
    FileOperations.create_thumbnail(f"{path}/{offer.primary_image}")


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


def get_image_path(db: Session, offer_id: int, image_name: str, offer_root_directory: str):
    offer = get_offer(db, offer_id, offer_root_directory)
    path = get_image_directory(offer_root_directory, offer.userid, offer_id)
    return f"{path}/{image_name}"


def get_thumbnail_path(db: Session, offer_id: int, offer_root_directory: str):
    offer = get_offer(db, offer_id, offer_root_directory)
    path = get_image_directory(offer_root_directory, offer.userid, offer_id)
    FileOperations.get_thumbnail_path(f"{path}/{offer.primaryimage}")


def delete_offer_image(db: Session, offer_id: int, image_name: str, offer_root_directory: str):
    path = get_image_path(db, offer_id, image_name, offer_root_directory)
    FileOperations.remove_file(path)


def add_description_to_results(result, offer_root_directory: str):
    for offer in result:
        offer.description = FileOperations.read_text_file(
            get_description_path(offer_root_directory, offer.userid, offer.id))
    return result


def get_description_path(offer_root_directory, user_id, offer_id):
    return f"{offer_root_directory}/{user_id}/{offer_id}/description.txt"


def get_image_directory(offer_root_directory, user_id, offer_id):
    return f"{offer_root_directory}/{user_id}/{offer_id}/images"


def get_short_description(description: str):
    short_description = description
    if len(short_description) > 50:
        short_description = description[0:49]
        last_blank = short_description.rfind(' ')
        while last_blank > 46:
            last_blank = short_description.rfind(' ',0,last_blank)
        short_description = description[0:last_blank]
    return short_description




