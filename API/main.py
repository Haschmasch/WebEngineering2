from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import Crud.Users
from API.Crud import Users, Offers, Categories, Subcategories
from API.Schemas import User, Offer, Category, Subcategory
from API import models
from database import SessionLocal, engine, config
import uvicorn
import datetime


def main():
    # Hier kann man was zum testen rein schreiben. Später kommt hier nur run_api() rein.
    db = SessionLocal()
    createUser = User.UserCreate(email="m.m@example.com",
                                 name="test",
                                 phone_number="1681561",
                                 timecreated=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
                                 password="123456")
    Users.create_user(db, createUser)


    createCategory = Category.CategoryCreate(name="TestCategory")
    res = Categories.create_category(db, createCategory)
    res1 = Categories.get_categories(db, 0, 100)
    createSubcategory = Subcategory.SubcategoryCreate(categoryid=res[0],
                                                      name="TestSubcategory")
    Subcategories.create_subcategory(db, createSubcategory)

    createOffer = Offer.OfferCreate(title="TestTitle",
                                    category_id=1,
                                    subcategory_id=1,
                                    price=float(1),
                                    currency="€",
                                    postcode="048654",
                                    city="TestCity",
                                    address="TestAddress",
                                    description="I am a test description",
                                    userid=1,
                                    timeposted=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
                                    primary_image="Test.jpg")

    Offers.create_offer(db, createOffer, config["OfferRootDir"])
    db.close()
    print("Hallo")


if __name__ == "__main__":
    main()
