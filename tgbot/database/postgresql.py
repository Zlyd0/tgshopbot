from asyncio import AbstractEventLoop

from asyncpg import create_pool

from tgbot.data.config import PG_USER, PG_PASS, PG_HOST, DB_NAME


# Основной класс БД
class Database:
    # Подключение к базам данных
    def __init__(self, loop: AbstractEventLoop):
        self.pool = loop.run_until_complete(
            create_pool(
                user=PG_USER,
                password=PG_PASS,
                host=PG_HOST,
                database=DB_NAME
            )
        )

    # Форматирование запроса без аргументов
    @staticmethod
    def update_format(sql, parameters: dict):
        sql += ', '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    # Форматирование запроса с аргументами
    @staticmethod
    def update_format_args(sql, parameters: dict):
        sql += " WHERE "
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())
