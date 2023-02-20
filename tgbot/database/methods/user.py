from tgbot.loader import db
from tgbot.misc.const_functions import get_date, get_unix


# Добавление пользователя
async def add_userx(user_id, user_login, user_name):
    await db.pool.execute("INSERT INTO storage_users(user_id, user_login, user_name, user_balance, user_refill, "
                          "user_date, user_unix) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                          user_id, user_login, user_name, 0, 0, get_date(), get_unix())


# Получение пользователя
async def get_userx(**kwargs):
    sql = "SELECT * FROM storage_users"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetchrow(sql, *parameters)


# Получение всех пользователей
async def get_all_usersx():
    sql = "SELECT * FROM storage_users"

    return await db.pool.fetch(sql)


# Редактирование пользователя
async def update_userx(user_id, **kwargs):
    sql = f"UPDATE storage_users SET "
    sql, parameters = db.update_format(sql, kwargs)
    sql += f"WHERE user_id = {user_id}"

    await db.pool.execute(sql, *parameters)
