import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import load_config
from handlers.book_handlers import book_router
from handlers.profile_handlers import profile_router
from handlers.register_handlers import register_router
from handlers.user_handlers import user_router
from keyboards.main_menu import create_main_menu
from services.send_rating import get_user_id


async def main():
    logging.basicConfig(level=logging.DEBUG)

    config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token,
                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(register_router)
    dp.include_router(profile_router)
    dp.include_router(book_router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        get_user_id,
        trigger="cron",
        day_of_week="fri",
        hour=10,
        minute=00,
        kwargs={"bot": bot}
    )
    scheduler.start()

    await create_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
