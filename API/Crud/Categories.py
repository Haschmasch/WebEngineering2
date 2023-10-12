from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from API import models
from API.Schemas import Category


def create_category(db: Session, category: Category.CategoryCreate):
    result = db.execute(insert(models.Category).values(name=category.name))
    db.commit()
    key = result.inserted_primary_key
    result.close()
    return key


def delete_category(db: Session, category_id: int):
    result = db.execute(delete(models.Category).where(models.Category.id == category_id))
    db.commit()
    return result.first()


def update_category(db: Session, category: Category.Category):
    result = db.execute(update(models.User)
                        .where(models.User.id == category.id)
                        .values(name=category.name))
    db.commit()
    return result.first()


def get_category(db: Session, category_id: int):
    result = db.execute(select(models.Category).where(models.Category.id == category_id))
    return result.first()


def get_categories(db: Session, first: int, last: int):
    result = db.execute(select(models.Category).offset(first).limit(last))
    return result.all()


def get_category_by_name(db: Session, name: str):
    result = db.execute(select(models.Category).where(models.Category.name == name))
    return result.first()

