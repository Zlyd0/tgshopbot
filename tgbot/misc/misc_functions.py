from asyncio import sleep
from json import loads
from os import system

from tgbot.data.config import get_admins, PATH_DATABASE, PG_USER, PG_PASS, PG_HOST, DB_NAME
from tgbot.database.methods.category import get_all_categoriesx, get_categoryx
from tgbot.database.methods.item import get_all_itemsx, get_itemsx
from tgbot.database.methods.position import get_all_positionsx, get_positionx
from tgbot.database.methods.purchase import get_all_purchasesx, get_purchasesx
from tgbot.database.methods.refill import get_all_refillx
from tgbot.database.methods.settings import update_settingsx, get_settingsx
from tgbot.database.methods.user import get_all_usersx, get_userx
from tgbot.loader import bot
from tgbot.misc.const_functions import get_unix, ded, get_date, convert_day
from tgbot.services.async_session import AsyncSession
from tgbot.utils.notify_admins import send_admins


# Автоматическая очистка ежедневной статистики после 00:00
async def update_profit_day():
    await send_admins(await get_statisctics())

    await update_settingsx(misc_profit_day=get_unix())


# Автоматическая очистка еженедельной статистики в понедельник 00:01
async def update_profit_week():
    await update_settingsx(misc_profit_week=get_unix())


# Автобэкапы БД для админов
async def autobackup_admin():
    system(f"pg_dump --dbname=postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}/{DB_NAME} -Fc -f {PATH_DATABASE}")

    for admin in get_admins():
        with open(PATH_DATABASE, "rb") as document:
            await bot.send_document(admin,
                                    document,
                                    caption=f"<b>📦 AUTOBACKUP</b>\n"
                                            f"🕰 <code>{get_date()}</code>")


# Получение faq
async def get_faq(user_id, send_message):
    get_user = await get_userx(user_id=user_id)

    if "{user_id}" in send_message:
        send_message = send_message.replace("{user_id}", f"<b>{get_user['user_id']}</b>")
    if "{username}" in send_message:
        send_message = send_message.replace("{username}", f"<b>{get_user['user_login']}</b>")
    if "{firstname}" in send_message:
        send_message = send_message.replace("{firstname}", f"<b>{get_user['user_name']}</b>")

    return send_message


# Загрузка текста на текстовый хостинг
async def upload_text(dp, get_text):
    aSession: AsyncSession = dp.bot['aSession']
    session = await aSession.get_session()

    spare_pass = False
    await sleep(0.5)

    response = await session.post("http://pastie.org/pastes/create",
                                  data={"language": "plaintext", "content": get_text})

    get_link = response.url
    if "create" in str(get_link):
        spare_pass = True

    if spare_pass:
        response = await session.post("https://www.friendpaste.com",
                                      json={"language": "text", "title": "", "snippet": get_text})

        get_link = loads((await response.read()).decode())['url']

    return get_link


# Получить информацию о позиции для админа
async def get_position_admin(position_id):
    get_settings = await get_settingsx()
    get_items = await get_itemsx(position_id=position_id)
    get_position = await get_positionx(position_id=position_id)
    get_purchases = await get_purchasesx(purchase_position_id=position_id)
    get_category = await get_categoryx(category_id=get_position['category_id'])

    show_profit_amount_all, show_profit_amount_day, show_profit_amount_week = 0, 0, 0
    show_profit_count_all, show_profit_count_day, show_profit_count_week = 0, 0, 0
    text_description = "<code>Отсутствует ❌</code>"
    photo_text = "<code>Отсутствует ❌</code>"
    get_photo = None

    if len(get_position['position_photo']) >= 5:
        photo_text = "<code>Присутствует ✅</code>"
        get_photo = get_position['position_photo']

    if get_position['position_description'] != "0":
        text_description = f"\n{get_position['position_description']}"

    for purchase in get_purchases:
        show_profit_amount_all += purchase['purchase_price']
        show_profit_count_all += purchase['purchase_count']

        if purchase['purchase_unix'] - get_settings['misc_profit_day'] >= 0:
            show_profit_amount_day += purchase['purchase_price']
            show_profit_count_day += purchase['purchase_count']
        if purchase['purchase_unix'] - get_settings['misc_profit_week'] >= 0:
            show_profit_amount_week += purchase['purchase_price']
            show_profit_count_week += purchase['purchase_count']

    get_message = ded(f"""
                  <b>📁 Позиция: <code>{get_position['position_name']}</code></b>
                  ➖➖➖➖➖➖➖➖➖➖
                  🗃 Категория: <code>{get_category['category_name']}</code>
                  💰 Стоимость: <code>{get_position['position_price']}₽</code>
                  📦 Количество: <code>{len(get_items)}шт</code>
                  📸 Изображение: {photo_text}
                  📜 Описание: {text_description}

                  💸 Продаж за День: <code>{show_profit_count_day}шт</code> - <code>{show_profit_amount_day}₽</code>
                  💸 Продаж за Неделю: <code>{show_profit_count_week}шт</code> - <code>{show_profit_amount_week}₽</code>
                  💸 Продаж за Всё время: <code>{show_profit_count_all}шт</code> - <code>{show_profit_amount_all}₽</code>
                  """)

    return get_message, get_photo


# Открытие своего профиля
async def open_profile_user(user_id):
    get_purchases = await get_purchasesx(user_id=user_id)
    get_user = await get_userx(user_id=user_id)

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24
    count_items = sum([items['purchase_count'] for items in get_purchases])

    return ded(f"""
           <b>👤 Ваш профиль:</b>
           ➖➖➖➖➖➖➖➖➖➖
           🆔 ID: <code>{get_user['user_id']}</code>
           💰 Баланс: <code>{get_user['user_balance']}₽</code>
           🎁 Куплено товаров: <code>{count_items}шт</code>
           🕰 Регистрация: <code>{get_user['user_date'].split(' ')[0]} ({convert_day(how_days)})</code>
           """)


# Открытие профиля при поиске
async def open_profile_admin(user_id):
    get_purchases = await get_purchasesx(user_id=int(user_id))
    get_user = await get_userx(user_id=int(user_id))

    how_days = int(get_unix() - get_user['user_unix']) // 60 // 60 // 24
    count_items = sum([items['purchase_count'] for items in get_purchases])

    return ded(f"""
           <b>👤 Профиль пользователя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a></b>
           ➖➖➖➖➖➖➖➖➖➖
           🆔 ID: <code>{get_user['user_id']}</code>
           👤 Логин: <b>@{get_user['user_login']}</b>
           Ⓜ Имя: <a href='tg://user?id={get_user['user_id']}'>{get_user['user_name']}</a>
           🕰 Регистрация: <code>{get_user['user_date']} ({convert_day(how_days)})</code>

           💰 Баланс: <code>{get_user['user_balance']}₽</code>
           💰 Всего пополнено: <code>{get_user['user_refill']}₽</code>
           🎁 Куплено товаров: <code>{count_items}шт</code>
           """)


# Статистика бота
async def get_statisctics():
    show_refill_amount_all, show_refill_amount_day, show_refill_amount_week = 0, 0, 0
    show_refill_count_all, show_refill_count_day, show_refill_count_week = 0, 0, 0
    show_profit_amount_all, show_profit_amount_day, show_profit_amount_week = 0, 0, 0
    show_profit_count_all, show_profit_count_day, show_profit_count_week = 0, 0, 0
    show_users_all, show_users_day, show_users_week, show_users_money = 0, 0, 0, 0

    get_categories = await get_all_categoriesx()
    get_positions = await get_all_positionsx()
    get_purchases = await get_all_purchasesx()
    get_refill = await get_all_refillx()
    get_settings = await get_settingsx()
    get_items = await get_all_itemsx()
    get_users = await get_all_usersx()

    for purchase in get_purchases:
        show_profit_amount_all += purchase['purchase_price']
        show_profit_count_all += purchase['purchase_count']

        if purchase['purchase_unix'] - get_settings['misc_profit_day'] >= 0:
            show_profit_amount_day += purchase['purchase_price']
            show_profit_count_day += purchase['purchase_count']
        if purchase['purchase_unix'] - get_settings['misc_profit_week'] >= 0:
            show_profit_amount_week += purchase['purchase_price']
            show_profit_count_week += purchase['purchase_count']

    for refill in get_refill:
        show_refill_amount_all += refill['refill_amount']
        show_refill_count_all += 1

        if refill['refill_unix'] - get_settings['misc_profit_day'] >= 0:
            show_refill_amount_day += refill['refill_amount']
            show_refill_count_day += 1
        if refill['refill_unix'] - get_settings['misc_profit_week'] >= 0:
            show_refill_amount_week += refill['refill_amount']
            show_refill_count_week += 1

    for user in get_users:
        show_users_money += user['user_balance']
        show_users_all += 1

        if user['user_unix'] - get_settings['misc_profit_day'] >= 0:
            show_users_day += 1
        if user['user_unix'] - get_settings['misc_profit_week'] >= 0:
            show_users_week += 1

    return ded(f"""
    <b>📊 СТАТИСТИКА БОТА</b>
    ➖➖➖➖➖➖➖➖➖➖
    <b>🔶 Пользователи 🔶</b>
    👤 Юзеров за День: <code>{show_users_day}</code>
    👤 Юзеров за Неделю: <code>{show_users_week}</code>
    👤 Юзеров за Всё время: <code>{show_users_all}</code>
     
    <b>🔶 Средства 🔶</b>
    💸 Продаж за День: <code>{show_profit_count_day}шт</code> - <code>{show_profit_amount_day}₽</code>
    💸 Продаж за Неделю: <code>{show_profit_count_week}шт</code> - <code>{show_profit_amount_week}₽</code>
    💸 Продаж за Всё время: <code>{show_profit_count_all}шт</code> - <code>{show_profit_amount_all}₽</code>
    💳 Средств в системе: <code>{show_users_money}₽</code>
    💰 Пополнений за День: <code>{show_refill_count_day}шт</code> - <code>{show_refill_amount_day}₽</code>
    💰 Пополнений за Неделю: <code>{show_refill_count_week}шт</code> - <code>{show_refill_amount_week}₽</code>
    💰 Пополнений за Всё время: <code>{show_refill_count_all}шт</code> - <code>{show_refill_amount_all}₽</code>
     
    <b>🔶 Прочее 🔶</b>
    🎁 Товаров: <code>{len(get_items)}шт</code>
    📁 Позиций: <code>{len(get_positions)}шт</code>
    🗃 Категорий: <code>{len(get_categories)}шт</code>
    """)
