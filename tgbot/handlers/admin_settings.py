from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import CantParseEntities

from tgbot.database.methods.settings import update_settingsx
from tgbot.database.methods.user import get_userx
from tgbot.filters.all_filters import IsAdmin
from tgbot.keyboards.inline_admin import settings_open_finl, turn_open_finl
from tgbot.loader import dp
from tgbot.misc.misc_functions import get_faq
from tgbot.utils.notify_admins import send_admins


# Изменение данных
@dp.message_handler(IsAdmin(), text="🖍 Изменить данные", state="*")
async def settings_data_edit(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🖍 Изменение данных бота.</b>", reply_markup=await settings_open_finl())


# Выключатели бота
@dp.message_handler(IsAdmin(), text="🕹 Выключатели", state="*")
async def settings_turn_edit(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("<b>🕹 Включение и выключение основных функций</b>", reply_markup=await turn_open_finl())


"""Выключатели"""


# Включение/выключение тех работ
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_work", state="*")
async def settings_turn_work(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = await get_userx(user_id=call.from_user.id)
    await update_settingsx(status_work=get_status)

    if get_status == "True":
        send_text = "🔴 Отправил бота на технические работы."
    else:
        send_text = "🟢 Вывел бота из технических работ."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=await turn_open_finl())


# Включение/выключение покупок
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_buy", state="*")
async def settings_turn_buy(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = await get_userx(user_id=call.from_user.id)
    await update_settingsx(status_buy=get_status)

    if get_status == "True":
        send_text = "🟢 Включил покупки в боте."
    else:
        send_text = "🔴 Выключил покупки в боте."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=await turn_open_finl())


# Включение/выключение пополнений
@dp.callback_query_handler(IsAdmin(), text_startswith="turn_pay", state="*")
async def settings_turn_pay(call: CallbackQuery, state: FSMContext):
    get_status = call.data.split(":")[1]

    get_user = await get_userx(user_id=call.from_user.id)
    await update_settingsx(status_refill=get_status)

    if get_status == "True":
        send_text = "🟢 Включил пополнения в боте."
    else:
        send_text = "🔴 Выключил пополнения в боте."

    await send_admins(
        f"👤 Администратор <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>\n"
        f"{send_text}", not_me=get_user['user_id'])

    await call.message.edit_reply_markup(reply_markup=await turn_open_finl())


"""Изменение данных"""


# Изменение поддержки
@dp.callback_query_handler(IsAdmin(), text_startswith="settings_edit_support", state="*")
async def settings_support_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_support")
    await call.message.edit_text("<b>☎ Отправьте ID пользователя.</b>\n"
                                 "❕ Вводимый ID должен быть пользователем бота.")


# Изменение FAQ
@dp.callback_query_handler(IsAdmin(), text_startswith="settings_edit_faq", state="*")
async def settings_faq_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state("here_settings_faq")
    await call.message.edit_text("<b>ℹ Введите новый текст для FAQ</b>\n"
                                 "❕ Вы можете использовать заготовленный синтаксис и HTML разметку:\n"
                                 "▶ <code>{username}</code>  - логин пользователя\n"
                                 "▶ <code>{user_id}</code>   - айди пользователя\n"
                                 "▶ <code>{firstname}</code> - имя пользователя")


# Принятие нового текста для FAQ
@dp.message_handler(IsAdmin(), state="here_settings_faq")
async def settings_faq_get(message: Message, state: FSMContext):
    get_message = await get_faq(message.from_user.id, message.text)

    try:
        cache_msg = await message.answer(get_message)
        await cache_msg.delete()

        await state.finish()
        await update_settingsx(misc_faq=message.text)

        await message.answer("<b>🖍 Изменение данных бота.</b>", reply_markup=await settings_open_finl())
    except CantParseEntities:
        await message.answer("<b>❌ Ошибка синтаксиса HTML.</b>\n"
                             "ℹ Введите новый текст для FAQ")


# Принятие нового айди для поддержки
@dp.message_handler(IsAdmin(), state="here_settings_support")
async def settings_support_get(message: Message, state: FSMContext):
    if message.text.isdigit():
        get_user = await get_userx(user_id=int(message.text))

        if get_user is not None:
            if len(get_user['user_login']) >= 1:
                await state.finish()
                await update_settingsx(misc_support=str(get_user['user_id']))

                await message.answer("<b>🖍 Изменение данных бота.</b>", reply_markup=await settings_open_finl())
            else:
                await message.answer("<b>❌ У пользователя отсутствует юзернейм.</b>\n"
                                     "☎ Отправьте ID пользователя.")
        else:
            await message.answer("<b>❌ Пользователь не был найден.</b>\n"
                                 "☎ Отправьте ID пользователя.")
    else:
        await message.answer("<b>❌ Данные были введены неверно.</b>\n"
                             "☎ Отправьте ID пользователя.")
