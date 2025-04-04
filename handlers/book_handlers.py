from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from sqlalchemy import insert, select, update

from database.connect import get_async_session
from database.models import Book, BookPoint, User
from filters.book_filters import BookTimeFilter
from keyboards.book_keyboards import create_list_book_keyboard, \
    create_time_keyboard
from lexicons.lexicon_book_ru import LEXICON_BOOK_RU
from services.book_services import TIME_DATA, calculate_point_from_time
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

    await message.answer(LEXICON_BOOK_RU["start_add_book_without_books"])


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
            ).returning(Book.id)
            result = await session.execute(book_query)
            await session.commit()
            book_id = result.scalar()
            select_book_query = select(Book).where(
                Book.id == book_id
            )
            book = await session.scalar(select_book_query)

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

        update_user_query = update(User).where(
            User.id == user.id
        ).values(minutes=User.minutes + TIME_DATA[key])
        await session.execute(update_user_query)

        await session.commit()

    text = (f"<b>Добавлено новое время чтения</b>\n\n"
            f"Книга: {data.get('book').title}\n"
            f"Время: {TIME_DATA[key]} минут")
    await callback.message.answer(text)


@book_router.message(StateFilter(BookState.time),
                     BookTimeFilter())
async def register_time(message: Message, state: FSMContext):
    points, minutes = calculate_point_from_time(message.text)
    user = await get_user_by_id(message.from_user.id)
    data = await state.get_data()
    await state.clear()

    async with get_async_session() as session:
        book_point_query = insert(BookPoint).values(
            book_id=data.get("book").id,
            user_id=user.id,
            time=minutes
        )
        await session.execute(book_point_query)

        update_user_query = update(User).where(
            User.id == user.id
        ).values(minutes=User.minutes + minutes)
        await session.execute(update_user_query)

        await session.commit()

    text = (f"<b>Добавлено новое время чтения</b>\n\n"
            f"Книга: {data.get('book').title}\n"
            f"Время: {minutes} минут")
    await message.answer(text)


@book_router.message(StateFilter(BookState.time))
async def error_register_time(message: Message):
    await message.answer(LEXICON_BOOK_RU["error_start_add_time"])
