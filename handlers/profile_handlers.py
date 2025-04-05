from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update

from database.connect import get_async_session
from database.models import BookPoint, User
from keyboards.profile_keyboards import create_profile_keyboard
from lexicons.lexicon_profile_ru import LEXICON_PROFILE_RU
from services.database_services import get_user_by_id
from services.profile_services import get_rating

profile_router = Router()
storage = MemoryStorage()


class ProfileState(StatesGroup):
    name = State()
    surname = State()
    age = State()


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


@profile_router.callback_query(lambda x: x.data in ("profile_change_name",
                                                    "profile_change_surname",
                                                    "profile_change_age"))
async def get_state_for_change_data(callback: CallbackQuery,
                                    state: FSMContext):
    if callback.data == "profile_change_name":
        await state.set_state(ProfileState.name)
        await callback.message.answer(LEXICON_PROFILE_RU["change_name"])
        return
    if callback.data == "profile_change_surname":
        await state.set_state(ProfileState.surname)
        await callback.message.answer(LEXICON_PROFILE_RU["change_surname"])
        return
    if callback.data == "profile_change_age":
        await state.set_state(ProfileState.age)
        await callback.message.answer(LEXICON_PROFILE_RU["change_age"])
        return


@profile_router.message(StateFilter(ProfileState.name),
                        lambda x: len(x.text.split(" ")) == 1)
async def finish_change_name(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    async with get_async_session() as session:
        update_user_query = update(User).where(
            User.id == user.id
        ).values(name=message.text.title())
        await session.execute(update_user_query)
        await session.commit()

    await state.clear()
    await message.answer(LEXICON_PROFILE_RU["changed"])
    await get_profile(message)


@profile_router.message(StateFilter(ProfileState.surname),
                        lambda x: len(x.text.split(" ")) == 1)
async def finish_change_surname(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    async with get_async_session() as session:
        update_user_query = update(User).where(
            User.id == user.id
        ).values(surname=message.text.title())
        await session.execute(update_user_query)
        await session.commit()

    await state.clear()
    await message.answer(LEXICON_PROFILE_RU["changed"])
    await get_profile(message)


@profile_router.message(StateFilter(ProfileState.age),
                        F.text.isdigit())
async def finish_change_surname(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    async with get_async_session() as session:
        update_user_query = update(User).where(
            User.id == user.id
        ).values(age=int(message.text))
        await session.execute(update_user_query)
        await session.commit()

    await state.clear()
    await message.answer(LEXICON_PROFILE_RU["changed"])
    await get_profile(message)


@profile_router.callback_query(F.data == "profile_watch_points")
async def profile_watch_points(callback: CallbackQuery):
    user = await get_user_by_id(callback.from_user.id)
    text = "<b>20 последних занятий чтением:</b>\n\n"
    async with get_async_session() as session:
        books_query = select(BookPoint).where(
            BookPoint.user_id == user.id
        ).order_by(BookPoint.id.desc()).limit(20)
        books = await session.scalars(books_query)

        for book in books:
            text += f" - Книга {book.book}, время чтения {book.time} минут\n"

    await callback.message.answer(text)

