from aiogram import Dispatcher

from tgbot.data.config import get_admins
from tgbot.keyboards.reply_all import menu_frep
from tgbot.loader import bot
from tgbot.misc.const_functions import ded


# Уведомление и проверка обновления при запуске бота
async def on_startup_notify(dp: Dispatcher):
    if len(get_admins()) >= 1:
        await send_admins(ded(f"""
                          <b>✅ Бот был успешно запущен</b>
                          <code>❗ Данное сообщение видят только администраторы бота.</code>
                          """),
                          markup="default")


# Рассылка сообщения всем администраторам
async def send_admins(message, markup=None, not_me=0):
    for admin in get_admins():
        if markup == "default":
            markup = menu_frep(admin)

        if str(admin) != str(not_me):
            await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
