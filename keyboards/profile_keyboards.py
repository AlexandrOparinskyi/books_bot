from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_profile_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="Изменить имя",
            callback_data="profile_change_name"
        ),
        InlineKeyboardButton(
            text="Изменить фамилию",
            callback_data="profile_change_surname"
        ),
        InlineKeyboardButton(
            text="Изменить возраст",
            callback_data="profile_change_age"
        ),
        InlineKeyboardButton(
            text="Статистика чтения",
            callback_data="profile_watch_points"
        ),
        width=2
    )
    return kb_builder.as_markup()
