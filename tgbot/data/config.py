from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(getenv("BOT_TOKEN"))  # Токен бота
PATH_DATABASE = "tgbot/data/database.backup"  # Путь к базе данных
PATH_LOGS = "tgbot/data/logs.log"  # Путь к логам
BOT_VERSION = "1.0"  # Версия бота

# Данные для подключения к базе данных
PG_USER = str(getenv("PG_USER"))  # Логин
PG_PASS = str(getenv("PG_PASS"))  # Пароль
PG_HOST = getenv("PG_HOST")  # IP адрес хоста
DB_NAME = str(getenv("DB_NAME"))  # Имя базы данных


# Получение администраторов бота
def get_admins():
    admins = str(getenv("ADMINS"))

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins:
        admins.remove("")
    while " " in admins:
        admins.remove(" ")
    while "\r" in admins:
        admins.remove("\r")
    while "\n" in admins:
        admins.remove("\n")

    admins = list(map(int, admins))

    return admins
