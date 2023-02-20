from tgbot.loader import db


# Добавление покупки
async def add_purchasex(user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price,
                        purchase_price_one, purchase_position_id, purchase_position_name, purchase_item, purchase_date,
                        purchase_unix, balance_before, balance_after):
    await db.pool.execute("INSERT INTO storage_purchases(user_id, user_login, user_name, purchase_receipt, "
                          "purchase_count, purchase_price, purchase_price_one, purchase_position_id, "
                          "purchase_position_name, purchase_item, purchase_date, purchase_unix, balance_before, "
                          "balance_after) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)",
                          user_id, user_login, user_name, purchase_receipt, purchase_count, purchase_price,
                          purchase_price_one, purchase_position_id, purchase_position_name, purchase_item,
                          purchase_date, purchase_unix, balance_before, balance_after
                          )


# Получение покупки
async def get_purchasex(**kwargs):
    sql = f"SELECT * FROM storage_purchases"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetchrow(sql, *parameters)


# Получение покупок
async def get_purchasesx(**kwargs):
    sql = f"SELECT * FROM storage_purchases"
    sql, parameters = db.update_format_args(sql, kwargs)

    return await db.pool.fetch(sql, *parameters)


# Получение всех покупок
async def get_all_purchasesx():
    sql = "SELECT * FROM storage_purchases"

    return await db.pool.fetch(sql)


# Последние 10 покупок
async def last_purchasesx(user_id, count):
    sql = f"SELECT * FROM storage_purchases WHERE user_id = $1 ORDER BY id DESC LIMIT {count}"

    return await db.pool.fetch(sql, user_id)
