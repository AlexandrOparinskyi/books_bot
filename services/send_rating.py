import time

from aiogram import Bot
from sqlalchemy import select

from database.connect import get_async_session
from database.models import User
from services.database_services import get_user_by_id
from services.profile_services import get_rating


async def send_rating(bot: Bot, user_id: int):
    user = await get_user_by_id(user_id)
    _, this_rating = await get_rating(user)

    text = "<b>10 лучших читателей:</b>\n\n"

    async with get_async_session() as session:
        users = await session.scalars(select(User).order_by(
            User.minutes.desc()
        ).limit(10))
        for user in users:
            text += (f"{user.name} {user.surname}, {user.minutes} "
                     f"минут чтения\n")

    text += f"\nВаше место в рейтинге - {this_rating}"

    await bot.send_message(chat_id=user_id, text=text)


async def get_user_id(bot: Bot):
    async with get_async_session() as session:
        users = await session.scalars(select(User))
        for user in users:
            try:
                await send_rating(bot, user.user_id)
            except:
                continue
