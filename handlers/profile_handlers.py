from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.profile_keyboards import create_profile_keyboard
from lexicons.lexicon_profile_ru import LEXICON_PROFILE_RU
from services.database_services import get_user_by_id

profile_router = Router()


@profile_router.message(Command(commands="profile"))
async def get_profile(message: Message):
    user = await get_user_by_id(message.from_user.id)
    if user is None:
        await message.answer(LEXICON_PROFILE_RU["user_not_exists"])
        return

    text = (f"<b>{user.name} {user.surname}</b>\n\n"
            f"У вас {user.minutes} минут чтения\n")
    keyboard = create_profile_keyboard()
    await message.answer(text, reply_markup=keyboard)

