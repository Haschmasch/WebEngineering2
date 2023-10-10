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
    offerid = Column(Integer, ForeignKey('offers.id'), index=True)
    creatorid = Column(Integer, ForeignKey('users.id'))
    timeopened = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)


class Following(Base):
    __tablename__ = 'followings'
    id = Column(Integer, Sequence('following_id_seq'), primary_key=True)
    offerid = Column(Integer, ForeignKey('offers.id'))
    userid = Column(Integer, ForeignKey('users.id'))
    timefollowed = Column(TIMESTAMP(timezone=True), nullable=False)


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, Sequence('offer_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    categoryid = Column(Integer, ForeignKey('categories.id'))
    subcategoryid = Column(Integer, ForeignKey('subcategories.id'))
    price = Column(Numeric(12, 4), CheckConstraint('price > 0'), nullable=True)
    currency = Column(CHAR(1))
    userid = Column(Integer, ForeignKey('users.id'))
    timeposted = Column(TIMESTAMP(timezone=True), nullable=False)
    closed = Column(Boolean)
    timeclosed = Column(TIMESTAMP(timezone=True))
    postcode = Column(String)
    city = Column(String)
    address = Column(String)


class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, Sequence('subcategory_id_seq'), primary_key=True)
    categoryid = Column(Integer, ForeignKey('categories.id'))
    name = Column(String(50))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False)
    passwordsalt = Column(Text, nullable=False)
    passwordhash = Column(Text, nullable=False)
    phonenumber = Column(Text)
    __table_args__ = (UniqueConstraint('name', 'email', name='ue_users'),)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    chatid = Column(Integer, ForeignKey('chats.id'), index=True)
    content = Column(String)
    timestamp = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)

