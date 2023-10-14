from API.setup_database import SessionLocal
from API.Crud import Offers, Chats
from API.init_database import init_db
from API.Schemas import Offer, Chat
from API.setup_api import run_api
import datetime
from API.Utils.ConfigManager import configuration



def main():
    init_db()
    # Hier kann man was zum testen rein schreiben. Später kommt hier nur run_api() rein.
    db = SessionLocal()
    '''
    createUser = User.UserCreate(email="m.m@example.com",
                                 name="test",
                                 phone_number="1681561",
                                 time_created=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
                                 password="123456")
    Users.create_user(db, createUser)
   

    createCategory = Category.CategoryCreate(name="TestCategory")
    res = Categories.create_category(db, createCategory)
    res1 = Categories.get_categories(db, 0, 100)
    createSubcategory = Subcategory.SubcategoryCreate(category_id=res.id,
                                                      name="TestSubcategory")
    Subcategories.create_subcategory(db, createSubcategory)
    '''
    createOffer = Offer.OfferCreate(title="Auto",
                                    category_id=28,
                                    subcategory_id=1,
                                    price=float(10.3),
                                    currency="€",
                                    postcode="048654",
                                    city="Hamburg",
                                    address="TestAddress",
                                    description="I am a test description",
                                    user_id=1,
                                    time_posted=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
                                    primary_image="Test.jpg")

    Offers.create_offer(db, createOffer, configuration.offer_root_dir)
    createChat = Chat.ChatCreate(offerid=1, creatorid=1,
                                 timeopened=datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
    Chats.create_chat(db, createChat)
    db.close()
    print("Hallo")
    run_api()


if __name__ == "__main__":
    main()
