import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from handlers.register_handlers import register_router
from handlers.user_handlers import user_router
from keyboards.main_menu import create_main_menu


async def main():
    logging.basicConfig(level=logging.DEBUG)

    config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token,
                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(register_router)

    await create_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
