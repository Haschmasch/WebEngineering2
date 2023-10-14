from API.Schemas.Category import Category
from API.Schemas.Subcategory import Subcategory
from API.Schemas.Offer import Offer
from API.Schemas.User import User


class SubcategoryWithCategory(Subcategory):
    related_category: Category


class CategoryWithSubcategories(Category):
    related_subcategories: list[Subcategory] = []


class SubcategoryWithOffers(Subcategory):
    related_offers: list[Offer] = []


class CategoryWithOffers(Category):
    related_offers: list[Offer] = []


class OfferWithRelations(Offer):
    related_subcategory: Subcategory = None
    related_category: Category = None
    related_user: User = None

