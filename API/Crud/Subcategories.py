from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from API import models
from API.Schemas import Subcategory


def create_subcategory(db: Session, subcategory: Subcategory.SubcategoryCreate):
    db_subcategory = models.Subcategory(name=subcategory.name, categoryid=subcategory.category_id)
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


def delete_subcategory(db: Session, subcategory_id):
    db.execute(delete(models.Subcategory).where(models.Subcategory.id == subcategory_id))
    db.commit()


def update_subcategory(db: Session, subcategory: Subcategory.Subcategory):
    result = db.scalars(update(models.Subcategory)
                        .returning(models.Subcategory)
                        .where(models.Subcategory.id == subcategory.id)
                        .values(name=subcategory.name, categoryid=subcategory.category_id))
    db.commit()
    return result.first()


def get_subcategory(db: Session, subcategory_id: int):
    result = db.scalars(select(models.Subcategory).where(models.Subcategory.id == subcategory_id))
    return result.first()


def get_subcategories(db: Session, first: int, last: int):
    result = db.scalars(select(models.Subcategory).offset(first).limit(last))
    return result.all()


def get_subcategories_by_category_id(db: Session, category_id: int):
    result = db.scalars(select(models.Subcategory).where(models.Subcategory.categoryid == category_id))
    return result.all()


def get_subcategory_by_name(db: Session, name: str):
    result = db.scalars(select(models.Subcategory).where(models.Subcategory.name == name))
    return result.first()
