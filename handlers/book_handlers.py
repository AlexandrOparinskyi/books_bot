from importlib.metadata import pass_none

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages
from sqlalchemy import insert, select, update

from database.connect import get_async_session
from database.models import Book, BookPoint, UserPoint
from keyboards.book_keyboards import create_list_book_keyboard, create_time_keyboard
from lexicons.lexicon_book_ru import LEXICON_BOOK_RU
from lexicons.lexicons_user_ru import LEXICON_USER_RU
from services.book_services import TIME_DATA
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

    keyboard = create_time_keyboard()
    await state.update_data({"book": book})
    await message.answer(LEXICON_BOOK_RU["start_add_time"],
                         reply_markup=keyboard)


@book_router.callback_query(StateFilter(BookState.book),
                            F.data.startswith("add_book_"))
async def register_book_cb(callback: CallbackQuery, state: FSMContext):
    index = callback.data.split("_")[2]
    user = await get_user_by_id(callback.from_user.id)
    await state.set_state(BookState.time)

    async with get_async_session() as session:
        book_query = select(Book).where(
            Book.user_id == user.id
        ).order_by(Book.id.desc())
        book = await session.scalars(book_query)

    keyboard = create_time_keyboard()
    await state.update_data({"book": book.all()[int(index)]})
    await callback.message.answer(LEXICON_BOOK_RU["start_add_time"],
                                  reply_markup=keyboard)


@book_router.callback_query(StateFilter(BookState.time),
                            F.data.startswith("add_time_"))
async def register_time_cb(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split("_")[2]
    data = await state.get_data()
    user = await get_user_by_id(callback.from_user.id)
    await state.clear()

    async with get_async_session() as session:
        book_point_query = insert(BookPoint).values(
            book_id=data.get("book").id,
            user_id=user.id,
            time=TIME_DATA[key]
        )
        await session.execute(book_point_query)

        user_point_query = select(UserPoint).where(
            UserPoint.user_id == user.id
        )
        user_point = await session.scalar(user_point_query)
        user_point.points += TIME_DATA[key] / 10

        await session.commit()

    text = (f"<b>Добавлено новое время чтения</b>\n\n"
            f"Книга: {data.get('book')}\n"
            f"Время: {TIME_DATA[key]} минут")
    await callback.message.answer(text)
