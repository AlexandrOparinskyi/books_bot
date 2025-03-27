from aiogram import Bot
from aiogram.types import BotCommand


async def create_main_menu(bot: Bot):
    main_menu = [
        BotCommand(
            command="/help",
            description="Помощь"
        ),
        BotCommand(
            command="/register",
            description="Регистрация"
        ),
        BotCommand(
            command="/profile",
            description="Мой профиль"
        )
    ]
    await bot.set_my_commands(main_menu)
