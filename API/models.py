from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, Text, Identity, UniqueConstraint, \
    TIMESTAMP, CheckConstraint, Numeric, CHAR
import datetime

from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(50))
    related_subcategories = relationship("Subcategory", back_populates="related_category", cascade="all, delete")
    related_offers = relationship("Offer", back_populates="related_category")


class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, Identity(), primary_key=True)
    categoryid = Column(Integer, ForeignKey('categories.id'))
    name = Column(String(50))
    related_category = relationship("Category", back_populates="related_subcategories")
    related_offers = relationship("Offer", back_populates="related_subcategory")


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, Identity(), primary_key=True)
    offerid = Column(Integer, ForeignKey('offers.id'), index=True)
    creatorid = Column(Integer, ForeignKey('users.id'))
    timeopened = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    related_offer = relationship("Offer", back_populates="related_chats")


class Following(Base):
    __tablename__ = 'followings'
    id = Column(Integer, Identity(), primary_key=True)
    offerid = Column(Integer, ForeignKey('offers.id'))
    userid = Column(Integer, ForeignKey('users.id'))
    timefollowed = Column(TIMESTAMP(timezone=True), nullable=False)
    related_offer = relationship("Offer", back_populates="related_followings")


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, Identity(), primary_key=True)
    title = Column(String(200), nullable=False)
    categoryid = Column(Integer, ForeignKey('categories.id'))
    subcategoryid = Column(Integer, ForeignKey('subcategories.id'))
    price = Column(Numeric(12, 4), CheckConstraint('price > 0'), nullable=True)
    currency = Column(CHAR(1))
    userid = Column(Integer, ForeignKey('users.id'))
    timeposted = Column(TIMESTAMP(timezone=True), nullable=False)
    closed = Column(Boolean, default=False)
    timeclosed = Column(TIMESTAMP(timezone=True))
    postcode = Column(String)
    city = Column(String)
    address = Column(String)
    primaryimage = Column(String)
    related_subcategory = relationship("Subcategory", back_populates="related_offers")
    related_category = relationship("Category", back_populates="related_offers")
    related_followings = relationship("Following", back_populates="related_offer")
    related_chats = relationship("Chat", back_populates="related_offer")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False)
    passwordsalt = Column(Text, nullable=False)
    passwordhash = Column(Text, nullable=False)
    phonenumber = Column(Text)
    timecreated = Column(TIMESTAMP(timezone=True), nullable=False)
    __table_args__ = (UniqueConstraint('name', 'email', name='ue_users'),)


