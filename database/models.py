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

    user_point = relationship("UserPoint", lazy="selectin")

    def __repr__(self):
        return f"{self.name} {self.surname}"


class UserPoint(Base):
    __tablename__ = 'user_points'

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    points = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.user_id} - {self.points} очков"
