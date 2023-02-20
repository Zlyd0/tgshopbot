from tgbot.loader import db
from tgbot.misc.const_functions import get_unix
from tgbot.utils.logging import bot_logger


# Создание всех таблиц для базы данных
async def create_dbx():
    # Создание базы данных с хранением данных пользователей
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_users(
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    user_login TEXT,
    user_name TEXT,
    user_balance INTEGER,
    user_refill INTEGER,
    user_date TEXT,
    user_unix INTEGER
    );""")
    bot_logger.info("DB was found(1/8)")

    # Создание базы данных с хранением данных платежных систем
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_payment(
    id SERIAL PRIMARY KEY,
    qiwi_login TEXT,
    qiwi_token TEXT,
    qiwi_secret TEXT,
    qiwi_nickname TEXT,
    way_form TEXT,
    way_number TEXT,
    way_nickname TEXT
    );""")
    
    if await db.pool.fetchrow("SELECT * FROM storage_payment") is None:
        await db.pool.execute("INSERT INTO storage_payment(qiwi_login, qiwi_token, qiwi_secret, qiwi_nickname, "
                              "way_form, way_number, way_nickname) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                              'None', 'None', 'None', 'None', 'False', 'False', 'False')
    bot_logger.info("DB was found(2/8)")

    # Создание базы данных с хранением настроек
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_settings(
    id SERIAL PRIMARY KEY,
    status_work TEXT,
    status_refill TEXT,
    status_buy TEXT,
    misc_faq TEXT,
    misc_support TEXT,
    misc_bot TEXT,
    misc_update TEXT,
    misc_profit_day INTEGER,
    misc_profit_week INTEGER
    );""")
    
    if await db.pool.fetchrow("SELECT * FROM storage_settings") is None:
        await db.pool.execute("INSERT INTO storage_settings(status_work, status_refill, status_buy, misc_faq, "
                              "misc_support, misc_bot, misc_update, misc_profit_day, misc_profit_week) VALUES ($1, "
                              "$2, $3, $4, $5, $6, $7, $8, $9)",
                              "True", "False", "False", "None", "None", "None", "False", get_unix(), get_unix())
    bot_logger.info("DB was found(3/8)")

    # Создание базы данных с хранением пополнений пользователей
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_refill(
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    user_login TEXT,
    user_name TEXT,
    refill_comment TEXT,
    refill_amount INTEGER,
    refill_receipt TEXT,
    refill_way TEXT,
    refill_date TIMESTAMP,
    refill_unix INTEGER
    );""")
    bot_logger.info("DB was found(4/8)")

    # Создание базы данных с хранением категорий
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_category(
    id SERIAL PRIMARY KEY,
    category_id INTEGER,
    category_name TEXT
    );""")
    bot_logger.info("DB was found(5/8)")

    # Создание базы данных с хранением позиций
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_position(
    id SERIAL PRIMARY KEY,
    position_id INTEGER,
    position_name TEXT,
    position_price INTEGER,
    position_description TEXT,
    position_photo TEXT,
    position_date TEXT,
    category_id INTEGER
    );""")
    bot_logger.info("DB was found(6/8)")

    # Создание базы данных с хранением товаров
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_item(
    id SERIAL PRIMARY KEY,
    item_id BIGINT,
    item_data TEXT,
    position_id INTEGER,
    category_id INTEGER,
    creator_id BIGINT,
    creator_name TEXT,
    add_date TEXT
    );""")
    bot_logger.info("DB was found(7/8)")

    # Создание базы данных с хранением покупок
    await db.pool.execute("""
    CREATE TABLE IF NOT EXISTS storage_purchases(
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    user_login TEXT,
    user_name TEXT,
    purchase_receipt TEXT,
    purchase_count INTEGER,
    purchase_price INTEGER,
    purchase_price_one INTEGER,
    purchase_position_id INTEGER,
    purchase_position_name TEXT,
    purchase_item TEXT,
    purchase_date TEXT,
    purchase_unix INTEGER,
    balance_before INTEGER,
    balance_after INTEGER
    );""")
    bot_logger.info("DB was found(8/8)")
