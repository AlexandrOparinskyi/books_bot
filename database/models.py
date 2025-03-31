from uuid import uuid4

from slugify import slugify
from sqlalchemy import (Column, Integer, BigInteger,
                        String, Boolean, ForeignKey)
from sqlalchemy.event import listens_for
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(150), nullable=True)
    name = Column(String(150), nullable=False)
    surname = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_banned = Column(Boolean, nullable=False, default=False)

    user_point = relationship("UserPoint", lazy="selectin")
    books = relationship("Book", lazy="selectin")

    def __repr__(self):
        return f"{self.name} {self.surname}"


class UserPoint(Base):
    __tablename__ = 'user_points'

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    points = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.user_id} - {self.points} очков"


class Book(Base):
    __tablename__ = "books"

    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    book_point = relationship("BookPoint", lazy="selectin")

    def __repr__(self):
        return self.title


class BookPoint(Base):
    __tablename__ = "book_points"

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    time = Column(Integer, nullable=False)
