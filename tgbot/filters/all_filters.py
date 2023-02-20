from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.data.config import get_admins
from tgbot.database.methods.settings import get_settingsx


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: Message):
        if message.from_user.id in get_admins():
            return True
        else:
            return False


# Проверка на возможность покупки товара
class IsBuy(BoundFilter):
    async def check(self, message: Message):
        get_settings = await get_settingsx()

        if get_settings['status_buy'] == "True" or message.from_user.id in get_admins():
            return False
        else:
            return True


# Проверка на возможность пополнения
class IsRefill(BoundFilter):
    async def check(self, message: Message):
        get_settings = await get_settingsx()

        if get_settings['status_refill'] == "True" or message.from_user.id in get_admins():
            return False
        else:
            return True


# Проверка на технические работы
class IsWork(BoundFilter):
    async def check(self, message: Message):
        get_settings = await get_settingsx()

        if get_settings['status_work'] == "False" or message.from_user.id in get_admins():
            return False
        else:
            return True
