from tgbot.loader import db


# Получение платежных систем
async def get_paymentx():
    sql = "SELECT * FROM storage_payment"

    return await db.pool.fetchrow(sql)


# Редактирование платежных систем
async def update_paymentx(**kwargs):
    sql = "UPDATE storage_payment SET "
    sql, parameters = db.update_format(sql, kwargs)

    await db.pool.execute(sql, *parameters)
