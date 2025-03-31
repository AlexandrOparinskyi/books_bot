from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from database.connect import get_async_session
from database.models import User, Book


async def create_list_book_keyboard(user: User) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    async with get_async_session() as session:
        books_query = select(Book).where(
            Book.user_id == user.id
        ).order_by(Book.id.desc())
        books = await session.scalars(books_query)
        kb_builder.row(
            *[InlineKeyboardButton(
                text=b.title[0].upper() + b.title[1:].lower(),
                callback_data=f"book_{i}"
            ) for i, b in enumerate(books.all()[:6])],
            width=1
        )

    return kb_builder.as_markup()
