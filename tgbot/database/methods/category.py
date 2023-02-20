from tgbot.loader import db


# Добавление категории
async def add_categoryx(category_id, category_name):
    await db.pool.execute("INSERT INTO storage_category (category_id, category_name) VALUES ($1, $2)",
                          category_id, category_name)


# Изменение категории
async def update_categoryx(category_id, **kwargs):
    sql = f"UPDATE storage_category SET "
    sql, parameters = db.update_format(sql, kwargs)
    sql += f" WHERE category_id = {category_id}"

    await db.pool.execute(sql, *parameters)


# Получение категории
async def get_categoryx(**kwargs):
    sql = f"SELECT * FROM storage_category"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetchrow(sql, *parameters)


# Получение всех категорий
async def get_all_categoriesx():
    sql = "SELECT * FROM storage_category"

    return await db.pool.fetch(sql)


# Удаление всех категорий
async def clear_categoryx():
    sql = "DELETE FROM storage_category"

    await db.pool.execute(sql)


# Удаление категории
async def remove_categoryx(**kwargs):
    sql = "DELETE FROM storage_category"
    sql, parameters = db.update_format_args(sql, kwargs)

    await db.pool.execute(sql, *parameters)
