from sqlalchemy import select

from database.connect import get_async_session
from database.models import User, Book


async def check_user_exists(user_id: int) -> bool:
    async with get_async_session() as session:
        user_query = select(User).where(User.user_id == user_id)
        user = await session.scalar(user_query)
        return user is not None


async def get_user_by_id(user_id: int) -> User:
    async with get_async_session() as session:
        user_query = select(User).where(User.user_id == user_id)
        user = await session.scalar(user_query)
        return user


async def check_exists_book(user: User, title: str) -> Book:
    async with get_async_session() as session:
        book_query = select(Book).where(
            Book.title == title.title(),
            Book.user_id == user.id
        )
        book = await session.scalar(book_query)
        return book
