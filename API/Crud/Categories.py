"""
Contains all create, read, update and delete operations for categories.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from API import models
from API.Schemas import Category
from API.Utils.Exceptions import EntryNotFoundException


def create_category(db: Session, category: Category.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if category is not None:
        db.execute(delete(models.Category).where(models.Category.id == category_id))
        db.commit()
    else:
        raise EntryNotFoundException(f"No database entry found for category_id: {category_id}")


def update_category(db: Session, category: Category.Category):
    result = db.scalars(update(models.Category)
                        .returning(models.Category)
                        .where(models.Category.id == category.id)
                        .values(name=category.name))
    db.commit()
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for category: {category.id}")


def get_category(db: Session, category_id: int):
    result = db.scalars(select(models.Category).where(models.Category.id == category_id))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for category_id: {category_id}")


def get_categories(db: Session, first: int, last: int):
    result = db.scalars(select(models.Category).offset(first).limit(last))
    res = result.all()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for first: {first}, last: {last}")


def get_category_by_name(db: Session, name: str):
    result = db.scalars(select(models.Category).where(models.Category.name == name))
    res = result.first()
    if res is not None:
        return res
    else:
        raise EntryNotFoundException(f"No database entry found for name: {name}")
