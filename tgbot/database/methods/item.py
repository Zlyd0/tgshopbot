from math import ceil
from random import randint

from tgbot.loader import db
from tgbot.misc.const_functions import clear_html, get_date


# Добавление товара
async def add_itemx(category_id, position_id, get_all_items, user_id, user_name):
    for item_data in get_all_items:
        if not item_data.isspace() and item_data != "":
            await db.pool.execute("INSERT INTO storage_item (item_id, item_data, position_id, category_id, "
                                  "creator_id, creator_name, add_date) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                                  randint(1000000000, 9999999999), clear_html(item_data.strip()), position_id,
                                  category_id, user_id, user_name, get_date()
                                  )


# Получение товара
async def get_itemx(**kwargs):
    sql = f"SELECT * FROM storage_item"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetchrow(sql, *parameters)


# Получение товаров
async def get_itemsx(**kwargs):
    sql = f"SELECT * FROM storage_item"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetch(sql, *parameters)


# Получение всех товаров
async def get_all_itemsx():
    sql = "SELECT * FROM storage_item"

    return await db.pool.fetch(sql)


# Очистка товаров
async def clear_itemx():
    sql = "DELETE FROM storage_item"

    await db.pool.execute(sql)


# Удаление товаров
async def remove_itemx(**kwargs):
    sql = "DELETE FROM storage_item"
    sql, parameters = db.update_format_args(sql, kwargs)

    await db.pool.execute(sql, *parameters)


# Покупка товаров
async def buy_itemx(get_items, get_count):
    split_len, send_count, save_items = 0, 0, []

    for select_send_item in get_items:
        if send_count != get_count:
            send_count += 1
            if get_count >= 2:
                select_data = f"{send_count}. {select_send_item['item_data']}"
            else:
                select_data = select_send_item['item_data']

            save_items.append(select_data)
            sql, parameters = db.update_format_args("DELETE FROM storage_item",
                                                    {"item_id": select_send_item['item_id']})
            await db.pool.execute(sql, *parameters)

            if len(select_data) >= split_len:
                split_len = len(select_data)
        else:
            break

    split_len += 1
    get_len = ceil(3500 / split_len)

    return save_items, send_count, get_len
