from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select, func

from database.connect import get_async_session
from database.models import BookPoint, User
from keyboards.profile_keyboards import create_profile_keyboard
from lexicons.lexicon_profile_ru import LEXICON_PROFILE_RU
from services.database_services import get_user_by_id
from services.profile_services import get_rating

profile_router = Router()


@profile_router.message(Command(commands="profile"))
async def get_profile(message: Message):
    user = await get_user_by_id(message.from_user.id)
    if user is None:
        await message.answer(LEXICON_PROFILE_RU["user_not_exists"])
        return

    text = (f"<b>{user.name} {user.surname}, {user.age} лет</b>\n\n"
            f"<b>Ваше недавние занятия чтением:</b>\n")
    async with get_async_session() as session:
        book_point_query = select(BookPoint).where(
            BookPoint.user_id == user.id
        ).order_by(BookPoint.id.desc()).limit(6)
        books = await session.scalars(book_point_query)
        times = 0
        for book in books:
            text += (f" -  Книга {book.book}, время чтения "
                     f"{book.time} минут\n")
            times += book.time
        text += f"\n<b>Общее время чтения: {times}</b>\n"

        _, rating = await get_rating(user)
        text += f"\n<b>Место в рейтинге: {rating}</b>"


    keyboard = create_profile_keyboard()
    await message.answer(text, reply_markup=keyboard)
