from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, Text, Identity, UniqueConstraint, \
    TIMESTAMP, CheckConstraint, Numeric, CHAR
import datetime

from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50))
    related_subcategories = relationship("Subcategory", back_populates="related_category", cascade="all, delete")
    related_offers = relationship("Offer", back_populates="related_category")


class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, Identity(), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String(50))
    related_category = relationship("Category", back_populates="related_subcategories")
    related_offers = relationship("Offer", back_populates="related_subcategory")


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, Identity(), primary_key=True)
    offer_id = Column(Integer, ForeignKey('offers.id'), index=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    time_opened = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    related_offer = relationship("Offer", back_populates="related_chats")


class Following(Base):
    __tablename__ = 'followings'
    id = Column(Integer, Identity(), primary_key=True)
    offer_id = Column(Integer, ForeignKey('offers.id'))
    userid = Column(Integer, ForeignKey('users.id'))
    time_followed = Column(TIMESTAMP(timezone=True), nullable=False)
    related_offer = relationship("Offer", back_populates="related_followings")


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, Identity(), primary_key=True)
    title = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'))
    price = Column(Numeric(12, 4), CheckConstraint('price > 0'), nullable=True)
    currency = Column(CHAR(1))
    user_id = Column(Integer, ForeignKey('users.id'))
    time_posted = Column(TIMESTAMP(timezone=True), nullable=False)
    closed = Column(Boolean, default=False)
    time_closed = Column(TIMESTAMP(timezone=True))
    postcode = Column(String)
    city = Column(String)
    address = Column(String)
    primary_image = Column(String)
    description = Column(String)
    short_description = Column(String(50))
    related_subcategory = relationship("Subcategory", back_populates="related_offers")
    related_category = relationship("Category", back_populates="related_offers")
    related_followings = relationship("Following", back_populates="related_offer", cascade="all, delete")
    related_chats = relationship("Chat", back_populates="related_offer", cascade="all, delete")
    related_user = relationship("User", back_populates="related_offers")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Identity(), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False)
    password_salt = Column(Text, nullable=False)
    password_hash = Column(Text, nullable=False)
    phone_number = Column(Text)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False)
    related_role = relationship("Roles", back_populates="related_users")
    related_offers = relationship("Offer", back_populates="related_user", cascade="all, delete")
    __table_args__ = (UniqueConstraint('name', 'email', name='ue_users'),)


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50), nullable=False)
    short_name = Column(String(25), nullable=False)
    related_users = relationship("User", back_populates="related_role")


