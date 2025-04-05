from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy import select

from database.connect import get_async_session
from database.models import User
from lexicons.lexicons_user_ru import LEXICON_USER_RU
from services.database_services import get_user_by_id
from services.profile_services import get_rating

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_USER_RU[message.text])


@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON_USER_RU[message.text])


@user_router.message(Command(commands="get_rating"))
async def get_users_rating(message: Message):
    text = "<b>Рейтинг читателей:</b>\n\n"

    async with get_async_session() as session:
        users_query = select(User).order_by(
            User.minutes.desc()
        ).limit(10)
        users = await session.scalars(users_query)
        for user in users:
            text += f" - {user}, время чтения {user.minutes} минут\n"

    this_user = await get_user_by_id(message.from_user.id)
    _, this_rating = await get_rating(this_user)
    text += f"\n<b>Ваш номер в рейтинге: {this_rating}</b>"
    await message.answer(text)
