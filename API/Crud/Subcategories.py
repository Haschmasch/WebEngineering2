"""
Contains all create, read, update and delete operations for subcategories.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
import models
from Schemas import Subcategory
from Utils.Exceptions import EntryNotFoundException


def create_subcategory(db: Session, subcategory: Subcategory.SubcategoryCreate):
    db_subcategory = models.Subcategory(name=subcategory.name, category_id=subcategory.category_id)
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


def delete_subcategory(db: Session, subcategory_id):
    subcategory = get_subcategory(db, subcategory_id)
    if subcategory is not None:
        db.execute(delete(models.Subcategory).where(models.Subcategory.id == subcategory_id))
        db.commit()
    else:
        raise EntryNotFoundException(f"No database entry found for subcategory_id: {subcategory_id}")


def update_subcategory(db: Session, subcategory: Subcategory.Subcategory):
    result = db.scalars(update(models.Subcategory)
                        .returning(models.Subcategory)
                        .where(models.Subcategory.id == subcategory.id)
                        .values(name=subcategory.name, category_id=subcategory.category_id))
    db.commit()
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for subcategory: {subcategory.id}")


def get_subcategory(db: Session, subcategory_id: int):
    result = db.scalars(select(models.Subcategory).where(models.Subcategory.id == subcategory_id))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for subcategory_id: {subcategory_id}")


def get_subcategories(db: Session, first: int, last: int):
    result = db.scalars(select(models.Subcategory).offset(first).limit(last))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for first: {first}, last: {last}")


def get_subcategories_by_category_id(db: Session, category_id: int):
    result = db.scalars(select(models.Subcategory).where(models.Subcategory.categoryid == category_id))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for category_id: {category_id}")


def get_subcategory_by_name(db: Session, name: str):
    result = db.scalars(select(models.Subcategory).where(models.Subcategory.name == name))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for name: {name}")
