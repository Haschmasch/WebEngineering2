from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, Text, Sequence, UniqueConstraint, \
    TIMESTAMP, CheckConstraint, Numeric, CHAR
import datetime
from .database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(50))


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, Sequence('chat_id_seq'), primary_key=True)
    offer_id = Column(Integer, ForeignKey('offers.id'), index=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    time_opened = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

class Following(Base):
    __tablename__ = 'followings'
    id = Column(Integer, Sequence('following_id_seq'), primary_key=True)
    offer_id = Column(Integer, ForeignKey('offers.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    time_followed = Column(TIMESTAMP(timezone=True), nullable=False)


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, Sequence('offer_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    subcategory_id = Column(Integer, ForeignKey('subcategories.id'))
    price = Column(Numeric(12, 4), CheckConstraint('price > 0'), nullable=True)
    currency = Column(CHAR(1))
    userid = Column(Integer, ForeignKey('users.id'))
    time_posted = Column(TIMESTAMP(timezone=True), nullable=False)
    closed = Column(Boolean)
    time_closed = Column(TIMESTAMP(timezone=True))
    postcode = Column(String)
    city = Column(String)
    address = Column(String)


class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, Sequence('subcategory_id_seq'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String(50))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False)
    password_hash = Column(Text, nullable=False)
    phone_number = Column(Text)
    __table_args__ = (UniqueConstraint('name', 'email', name='ue_users'),)



