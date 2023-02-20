import logging as bot_logger

from colorlog import ColoredFormatter

from tgbot.data.config import PATH_LOGS

# Формат логирования
log_formatter_file = bot_logger.Formatter("%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s")
log_formatter_console = ColoredFormatter(
    "%(purple)s%(levelname)s %(blue)s|%(purple)s %(asctime)s %(blue)s|%(purple)s %(filename)s:%(lineno)d %(blue)s|%("
    "purple)s %(message)s%(red)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

# Логирование в файл tgbot/data/logs.log
file_handler = bot_logger.FileHandler(PATH_LOGS, "w", "utf-8")
file_handler.setFormatter(log_formatter_file)


# Логирование в консоль
console_handler = bot_logger.StreamHandler()
console_handler.setFormatter(log_formatter_console)

# Подключение настроек логирования
bot_logger.basicConfig(
    format="%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s",
    level=bot_logger.INFO,
    handlers=[
        file_handler,
        console_handler
    ]
)
