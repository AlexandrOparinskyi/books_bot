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
                callback_data=f"add_book_{i}"
            ) for i, b in enumerate(books.all()[:6])],
            width=1
        )

    return kb_builder.as_markup()


def create_time_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="30 минут",
            callback_data="add_time_30m"
        ),
        InlineKeyboardButton(
            text="1 час",
            callback_data="add_time_1h"
        ),
        InlineKeyboardButton(
            text="1 час 30 минут",
            callback_data="add_time_1h30m"
        ),
        InlineKeyboardButton(
            text="2 часа",
            callback_data="add_time_2h"
        ),
        InlineKeyboardButton(
            text="2 часа 30 минут",
            callback_data="add_time_2h30ь"
        ),
        InlineKeyboardButton(
            text="3 часа",
            callback_data="add_time_3h"
        ),
        width=2
    )
    return kb_builder.as_markup()
