from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.database.methods.payment import get_paymentx
from tgbot.database.methods.settings import get_settingsx, update_settingsx
from tgbot.database.methods.user import get_userx


# Поиск профиля
def profile_search_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("💰 Изменить баланс", callback_data=f"admin_user_balance_set:{user_id}"),
        InlineKeyboardButton("💰 Выдать баланс", callback_data=f"admin_user_balance_add:{user_id}")
    ).add(
        InlineKeyboardButton("🎁 Покупки", callback_data=f"admin_user_purchases:{user_id}"),
        InlineKeyboardButton("💌 Отправить СМС", callback_data=f"admin_user_message:{user_id}")
    ).add(
        InlineKeyboardButton("🔄 Обновить", callback_data=f"admin_user_refresh:{user_id}")
    )

    return keyboard


# Возвращение к профилю
def profile_search_return_finl(user_id):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("❌ Отменить", callback_data=f"admin_user_refresh:{user_id}"),
    )

    return keyboard


# Способы пополнения
async def payment_choice_finl():
    keyboard = InlineKeyboardMarkup()
    get_payments = await get_paymentx()

    status_form_kb = InlineKeyboardButton("✅", callback_data="change_payment:Form:False")
    status_number_kb = InlineKeyboardButton("✅", callback_data="change_payment:Number:False")
    status_nickname_kb = InlineKeyboardButton("✅", callback_data="change_payment:Nickname:False")

    if get_payments['way_form'] == "False":
        status_form_kb = InlineKeyboardButton("❌", callback_data="change_payment:Form:True")
    if get_payments['way_number'] == "False":
        status_number_kb = InlineKeyboardButton("❌", callback_data="change_payment:Number:True")
    if get_payments['way_nickname'] == "False":
        status_nickname_kb = InlineKeyboardButton("❌", callback_data="change_payment:Nickname:True")

    keyboard.add(
        InlineKeyboardButton("📋 По форме", url="https://vk.cc/bYjKGM"), status_form_kb
    ).row(
        InlineKeyboardButton("📞 По номеру", url="https://vk.cc/bYjKEy"), status_number_kb
    ).row(
        InlineKeyboardButton("Ⓜ По никнейму", url="https://vk.cc/c8s66X"), status_nickname_kb
    )

    return keyboard


# Кнопки с настройками
async def settings_open_finl():
    keyboard = InlineKeyboardMarkup()

    get_settings = await get_settingsx()

    if get_settings['misc_support'].isdigit():
        get_user = await get_userx(user_id=int(get_settings['misc_support']))

        if get_user is not None:
            support_kb = InlineKeyboardButton(f"@{get_user['user_login']} ✅", callback_data="settings_edit_support")
        else:
            support_kb = InlineKeyboardButton("Не установлены ❌", callback_data="settings_edit_support")
            await update_settingsx(misc_support="None")
    else:
        support_kb = InlineKeyboardButton("Не установлены ❌", callback_data="settings_edit_support")

    if "None" == get_settings['misc_faq']:
        faq_kb = InlineKeyboardButton("Не установлено ❌", callback_data="settings_edit_faq")
    else:
        faq_kb = InlineKeyboardButton(f"{get_settings['misc_faq'][:15]}... ✅", callback_data="settings_edit_faq")

    keyboard.add(
        InlineKeyboardButton("ℹ FAQ", callback_data="..."), faq_kb
    ).add(
        InlineKeyboardButton("☎ Поддержка", callback_data="..."), support_kb
    )

    return keyboard


# Выключатели
async def turn_open_finl():
    keyboard = InlineKeyboardMarkup()

    get_settings = await get_settingsx()

    status_buy_kb = InlineKeyboardButton("Включены ✅", callback_data="turn_buy:False")
    status_work_kb = InlineKeyboardButton("Включены ✅", callback_data="turn_work:False")
    status_pay_kb = InlineKeyboardButton("Включены ✅", callback_data="turn_pay:False")

    if get_settings['status_buy'] == "False":
        status_buy_kb = InlineKeyboardButton("Выключены ❌", callback_data="turn_buy:True")
    if get_settings['status_work'] == "False":
        status_work_kb = InlineKeyboardButton("Выключены ❌", callback_data="turn_work:True")
    if get_settings['status_refill'] == "False":
        status_pay_kb = InlineKeyboardButton("Выключены ❌", callback_data="turn_pay:True")

    keyboard.row(
        InlineKeyboardButton("⛔ Тех. работы", callback_data="..."), status_work_kb
    ).row(
        InlineKeyboardButton("💰 Пополнения", callback_data="..."), status_pay_kb
    ).row(
        InlineKeyboardButton("🎁 Покупки", callback_data="..."), status_buy_kb
    )

    return keyboard


# Изменение категории
def category_edit_open_finl(category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🏷 Изм. название", callback_data=f"category_edit_name:{category_id}:{remover}"),
        InlineKeyboardButton("📁 Добавить позицию", callback_data=f"position_create_open:{category_id}"),
    ).add(
        InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"catategory_edit_swipe:{remover}"),
        InlineKeyboardButton("❌ Удалить", callback_data=f"category_edit_delete:{category_id}:{remover}")
    )

    return keyboard


# Кнопки с удалением категории
def category_edit_delete_finl(category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("❌ Да, удалить", callback_data=f"category_delete:{category_id}:yes:{remover}"),
        InlineKeyboardButton("✅ Нет, отменить", callback_data=f"category_delete:{category_id}:not:{remover}")
    )

    return keyboard


# Отмена изменения категории и возвращение
def category_edit_cancel_finl(category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("❌ Отменить", callback_data=f"category_edit_open:{category_id}:{remover}"),
    )

    return keyboard


# Кнопки при открытии позиции для изменения
def position_edit_open_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("🏷 Изм. название", callback_data=f"position_edit_name:{position_id}:{category_id}:"
                                                              f"{remover}"),
        InlineKeyboardButton("💰 Изм. цену", callback_data=f"position_edit_price:{position_id}:{category_id}:{remover}"),
    ).add(
        InlineKeyboardButton("📜 Изм. описание", callback_data=f"position_edit_description:{position_id}:{category_id}:"
                                                              f"{remover}"),
        InlineKeyboardButton("📸 Изм. фото", callback_data=f"position_edit_photo:{position_id}:{category_id}:{remover}"),
    ).add(
        InlineKeyboardButton("🗑 Очистить", callback_data=f"position_edit_clear:{position_id}:{category_id}:{remover}"),
        InlineKeyboardButton("🎁 Добавить товары", callback_data=f"products_add_position_open:{position_id}:"
                                                                f"{category_id}"),
    ).add(
        InlineKeyboardButton("📥 Товары", callback_data=f"position_edit_items:{position_id}:{category_id}:{remover}"),
        InlineKeyboardButton("❌ Удалить", callback_data=f"position_edit_delete:{position_id}:{category_id}:{remover}"),
    ).add(
        InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"position_edit_swipe:{category_id}:{remover}"),
    )

    return keyboard


# Подтверждение удаления позиции
def position_edit_delete_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("❌ Да, удалить", callback_data=f"position_delete:yes:{position_id}:{category_id}:"
                                                            f"{remover}"),
        InlineKeyboardButton("✅ Нет, отменить", callback_data=f"position_delete:not:{position_id}:{category_id}:"
                                                              f"{remover}")
    )

    return keyboard


# Подтверждение очистки позиции
def position_edit_clear_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("❌ Да, очистить", callback_data=f"position_clear:yes:{position_id}:{category_id}:"
                                                             f"{remover}"),
        InlineKeyboardButton("✅ Нет, отменить", callback_data=f"position_clear:not:{position_id}:{category_id}:"
                                                              f"{remover}")
    )

    return keyboard


# Отмена изменения позиции и возвращение
def position_edit_cancel_finl(position_id, category_id, remover):
    keyboard = InlineKeyboardMarkup(
    ).add(
        InlineKeyboardButton("❌ Отменить", callback_data=f"position_edit_open:{position_id}:{category_id}:{remover}"),
    )

    return keyboard
