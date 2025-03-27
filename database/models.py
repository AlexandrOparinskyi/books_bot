from sqlalchemy import Column, Integer, BigInteger, String, Boolean
from sqlalchemy.orm import DeclarativeBase


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

    def __repr__(self):
        return f"{self.name} {self.surname}"
