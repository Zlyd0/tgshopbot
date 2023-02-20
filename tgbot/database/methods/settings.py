from tgbot.loader import db


# Получение настроек
async def get_settingsx():
    sql = "SELECT * FROM storage_settings"

    return await db.pool.fetchrow(sql)


# Редактирование настроек
async def update_settingsx(**kwargs):
    sql = "UPDATE storage_settings SET "
    sql, parameters = db.update_format(sql, kwargs)

    await db.pool.execute(sql, *parameters)
