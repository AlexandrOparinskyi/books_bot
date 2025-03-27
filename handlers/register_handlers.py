from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from lexicons.lexicon_register_ru import LEXICON_REGISTER_RU

register_router = Router()
storage = MemoryStorage()


class RegisterState(StatesGroup):
    name = State()
    age = State()


@register_router.message(Command(commands="register"))
async def start_register(message: Message, state: FSMContext):
    await state.set_state(RegisterState.name)
    await message.answer(LEXICON_REGISTER_RU[message.text])


@register_router.message(StateFilter(RegisterState.name),
                         lambda x: len(x.text.split(" ")) == 2)
async def register_name(message: Message, state: FSMContext):
    name, surname = message.text.split(" ")
    await state.update_data({"name": name, "surname": surname})
    await state.set_state(RegisterState.age)
    await message.answer(LEXICON_REGISTER_RU["register_name"])


@register_router.message(StateFilter(RegisterState.name))
async def error_register_name(message: Message):
    await message.answer(LEXICON_REGISTER_RU["error_register_name"])


@register_router.message(StateFilter(RegisterState.age),
                         lambda x: x.text.isdigit() and 0 < int(x.text) < 100)
async def register_age(message: Message, state: FSMContext):
    await state.update_data({"age": int(message.text)})
    await state.clear()
    await message.answer(LEXICON_REGISTER_RU["register_age"])


@register_router.message(StateFilter(RegisterState.age))
async def error_register_age(message: Message):
    await message.answer(LEXICON_REGISTER_RU["error_register_age"])
