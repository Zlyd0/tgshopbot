from asyncio import get_event_loop

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.data.config import BOT_TOKEN
from tgbot.database.postgresql import Database

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

scheduler = AsyncIOScheduler()
db = Database(get_event_loop())
