from os import system
from sys import platform

from aiogram import Dispatcher
from aiogram.utils.executor import start_polling

from tgbot.data.config import get_admins
from tgbot.database.create_table import create_dbx
from tgbot.handlers import dp
from tgbot.loader import scheduler
from tgbot.middlewares import setup_middlewares
from tgbot.utils.logging import bot_logger
from tgbot.misc.misc_functions import update_profit_week, update_profit_day, autobackup_admin
from tgbot.services.async_session import AsyncSession
from tgbot.utils.notify_admins import on_startup_notify
from tgbot.utils.set_bot_commands import set_commands


# Запуск шедулеров
async def scheduler_start():
    scheduler.add_job(update_profit_week, "cron", day_of_week="mon", hour=00, minute=1)
    scheduler.add_job(update_profit_day, "cron", hour=00)
    scheduler.add_job(autobackup_admin, "cron", hour=00)


# Выполнение функции после запуска бота
async def on_startup(dp: Dispatcher):
    aSession = AsyncSession()
    dp.bot['aSession'] = aSession

    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)

    await create_dbx()
    setup_middlewares(dp)

    await set_commands(dp)
    await scheduler_start()
    await on_startup_notify(dp)

    bot_logger.warning("BOT WAS STARTED")

    if len(get_admins()) == 0:
        bot_logger.warning("ENTER ADMIN ID IN .env")


# Выполнение функции после выключения бота
async def on_shutdown(dp: Dispatcher):
    aSession: AsyncSession = dp.bot['aSession']
    await aSession.close()

    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()

    if platform.startswith("win"):
        system("cls")
    else:
        system("clear")


# Запуск бота
if __name__ == "__main__":
    scheduler.start()
    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
