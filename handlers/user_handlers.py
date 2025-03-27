from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from lexicons.lexicons_user_ru import LEXICON_USER_RU

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_USER_RU[message.text])


@user_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON_USER_RU[message.text])
