from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.database_services import get_user_by_id

profile_router = Router()


@profile_router.message(Command(commands="profile"))
async def get_profile(message: Message):
    user = await get_user_by_id(message.from_user.id)
    text = (f"{user.name}\n"
            f"{user.surname}\n"
            f"{user.user_point[0].points} очков\n")
    await message.answer(text)
