from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from .. import models
from ..Schemas import Subcategory


def create_subcategory(db: Session, subcategory: Subcategory.SubcategoryCreate):
    result = db.execute(insert(models.Subcategory).values(name=subcategory.name, categoryid=subcategory.categoryid))
    return result.first()


def delete_subcategory(db: Session, subcategory_id):
    result = db.execute(delete(models.Subcategory).where(models.Subcategory.id == subcategory_id))
    return result.first()


def update_subcategory(db: Session, subcategory: Subcategory.Subcategory):
    result = db.execute(update(models.Subcategory)
                        .where(models.Subcategory.id == subcategory.id)
                        .values(name=subcategory.name, categoryid=subcategory.categoryid))
    return result.first()


def get_subcategory(db: Session, subcategory_id: int):
    result = db.execute(select(models.Subcategory).where(models.Subcategory.id == subcategory_id))
    return result.first()


def get_subcategories(db: Session, first: int, last: int):
    result = db.execute(select(models.Subcategory).offset(first).limit(last))
    return result.all()


def get_subcategories_by_category_id(db: Session, category_id: int):
    result = db.execute(select(models.Subcategory).where(models.Subcategory.categoryid == category_id))
    return result.all()


def get_subcategory_by_name(db: Session, name: str):
    result = db.execute(select(models.Subcategory).where(models.Subcategory.name == name))
    return result.first()
