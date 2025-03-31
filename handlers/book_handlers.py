from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages
from sqlalchemy import insert

from database.connect import get_async_session
from database.models import Book
from keyboards.book_keyboards import create_list_book_keyboard
from lexicons.lexicon_book_ru import LEXICON_BOOK_RU
from lexicons.lexicons_user_ru import LEXICON_USER_RU
from services.database_services import get_user_by_id, check_exists_book

book_router = Router()
storage = MemoryStorage()


class BookState(StatesGroup):
    book = State()
    time = State()


@book_router.message(Command(commands="add_book"))
async def start_add_book(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    if user is None:
        await message.answer(LEXICON_BOOK_RU["user_not_exists"])
        return

    await state.set_state(BookState.book)

    if user.books:
        keyboard = await create_list_book_keyboard(user)
        await message.answer(LEXICON_BOOK_RU["start_add_book_with_books"],
                             reply_markup=keyboard)
        return

    await message.answer(LEXICON_USER_RU["start_add_book_without_books"])


@book_router.message(StateFilter(BookState.book))
async def register_book(message: Message, state: FSMContext):
    await state.set_state(BookState.time)
    user = await get_user_by_id(message.from_user.id)
    book = await check_exists_book(user, message.text)

    if book is None:
        async with get_async_session() as session:
            book_query = insert(Book).values(
                title=message.text.title(),
                user_id=user.id
            ).returning(Book.title)
            result = await session.execute(book_query)
            await session.commit()
            book = result.scalar()

    await state.update_data({"book": book})
    await message.answer(LEXICON_BOOK_RU["start_add_time"])
