from sqlalchemy import (Column, Integer, BigInteger,
                        String, Boolean, ForeignKey)
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
    minutes = Column(Integer, nullable=False, default=0)

    books = relationship("Book", lazy="selectin")

    def __repr__(self):
        return f"{self.name} {self.surname}"


class Book(Base):
    __tablename__ = "books"

    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    book_point = relationship("BookPoint",
                              back_populates="book",
                              lazy="selectin")

    def __repr__(self):
        return self.title


class BookPoint(Base):
    __tablename__ = "book_points"

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    time = Column(Integer, nullable=False)

    book = relationship("Book",
                        back_populates="book_point",
                        lazy="selectin")
