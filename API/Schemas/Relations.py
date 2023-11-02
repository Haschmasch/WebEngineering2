"""
Schemas for the communication over the api.
Contains mixed schemas representing the relations between the database models.
"""

from Schemas.Category import Category
from Schemas.Subcategory import Subcategory
from Schemas.Offer import Offer
from Schemas.User import User
from Schemas.Following import Following
from Schemas.Chat import Chat


class OfferWithRelations(Offer):
    related_subcategory: Subcategory | None = None
    related_category: Category | None = None
    related_user: User | None = None


class OfferWithCategoryRelations(Offer):
    related_subcategory: Subcategory | None = None
    related_user: User | None = None


class OfferWithSubcategoryRelations(Offer):
    related_category: Category | None = None
    related_user: User | None = None


class OfferWithUserRelations(Offer):
    related_subcategory: Subcategory | None = None
    related_category: Category | None = None


class FollowingWithOffer(Following):
    related_offer: Offer | None = None


class SubcategoryWithCategory(Subcategory):
    related_category: Category


class CategoryWithSubcategories(Category):
    related_subcategories: list[Subcategory] = []


class SubcategoryWithOffers(Subcategory):
    related_offers: list[OfferWithSubcategoryRelations] = []


class CategoryWithOffers(Category):
    related_offers: list[OfferWithCategoryRelations] = []


class UserWithOffers(User):
    related_offers: list[OfferWithUserRelations] = []


class ChatWithOffer(Chat):
    related_offer: OfferWithRelations

