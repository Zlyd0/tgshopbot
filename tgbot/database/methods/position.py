from tgbot.loader import db
from tgbot.misc.const_functions import get_date


# Добавление категории
async def add_positionx(position_id, position_name, position_price, position_description, position_photo, category_id):
    await db.pool.execute("INSERT INTO storage_position (position_id, position_name, position_price, "
                          "position_description, position_photo, position_date, category_id) VALUES ($1, $2, $3, $4, "
                          "$5, $6, $7)",
                          position_id, position_name, position_price, position_description, position_photo, get_date(),
                          category_id)


# Изменение позиции
async def update_positionx(position_id, **kwargs):
    sql = f"UPDATE storage_position SET "
    sql, parameters = db.update_format(sql, kwargs)
    sql += f"WHERE position_id = {position_id}"

    await db.pool.execute(sql, *parameters)


# Получение категории
async def get_positionx(**kwargs):
    sql = f"SELECT * FROM storage_position"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetchrow(sql, *parameters)


# Получение категорий
async def get_positionsx(**kwargs):
    sql = f"SELECT * FROM storage_position"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetch(sql, *parameters)


# Получение всех категорий
async def get_all_positionsx():
    sql = "SELECT * FROM storage_position"

    return await db.pool.fetch(sql)


# Удаление всех позиций
async def clear_positionx():
    sql = "DELETE FROM storage_position"

    await db.pool.execute(sql)


# Удаление позиции
async def remove_positionx(**kwargs):
    sql = "DELETE FROM storage_position"
    sql, parameters = db.update_format_args(sql, kwargs)

    await db.pool.execute(sql, *parameters)
