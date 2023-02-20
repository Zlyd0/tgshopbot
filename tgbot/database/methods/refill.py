from tgbot.loader import db


# Добавление пополнения
async def add_refillx(user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt,
                      refill_way, refill_date, refill_unix):
    await db.pool.execute("INSERT INTO storage_refill(user_id, user_login, user_name, refill_comment, refill_amount, "
                          "refill_receipt, refill_way, refill_date, refill_unix) VALUES ($1, $2, $3, $4, $5, $6, $7, "
                          "$8, $9)",
                          user_id, user_login, user_name, refill_comment, refill_amount, refill_receipt, refill_way,
                          refill_date, refill_unix
                          )


# Получение пополнения
async def get_refillx(**kwargs):
    sql = f"SELECT * FROM storage_refill"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetchrow(sql, *parameters)


# Получение всех пополнений
async def get_all_refillx():
    sql = "SELECT * FROM storage_refill"

    return await db.pool.fetch(sql)
