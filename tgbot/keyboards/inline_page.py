from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.database.methods.category import get_all_categoriesx
from tgbot.database.methods.item import get_itemsx
from tgbot.database.methods.position import get_positionsx

"""Изменение категории"""


# Стартовые страницы выбора категории для изменения
async def category_edit_swipe_fp(remover):
    get_categories = await get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                              callback_data=f"category_edit_open:{get_categories[a]['category_id']}:"
                                                            f"{remover}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}")
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"catategory_edit_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"catategory_edit_swipe:{remover + 10}"),
        )

    return keyboard


"""Создание позиции"""


# Страницы выбора категории для добавления позиции
async def position_create_swipe_fp(remover):
    get_categories = await get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                              callback_data=f"position_create_open:{get_categories[a]['category_id']}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"position_create_swipe:{remover + 10}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"position_create_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"position_create_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"position_create_swipe:{remover + 10}"),
        )

    return keyboard


"""Изменение позиции"""


# Стартовые страницы категорий при изменении позиции
async def position_edit_category_swipe_fp(remover):
    get_categories = await get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                              callback_data=f"position_edit_category_open:"
                                                            f"{get_categories[a]['category_id']}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"position_edit_category_swipe:{remover + 10}")
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"position_edit_category_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸",
                                 callback_data="...")
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"position_edit_category_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸",
                                 callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"position_edit_category_swipe:{remover + 10}"),
        )

    return keyboard


# Стартовые страницы позиций для их изменения
async def position_edit_swipe_fp(remover, category_id):
    get_positions = await get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_positions):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = await get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(InlineKeyboardButton(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"position_edit_open:{get_positions[a]['position_id']}:{category_id}:{remover}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"position_edit_swipe:{category_id}:{remover + 10}")
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"position_edit_swipe:{category_id}:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_positions) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"position_edit_swipe:{category_id}:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"position_edit_swipe:{category_id}:{remover + 10}"),
        )
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩", callback_data="position_edit_category_swipe:0"))

    return keyboard


"Добавление товаров"


# Страницы категорий при добавлении товара
async def products_add_category_swipe_fp(remover):
    get_categories = await get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                              callback_data=f"products_add_category_open:"
                                                            f"{get_categories[a]['category_id']}:{remover}"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"products_add_category_swipe:{remover + 10}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"products_add_category_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"products_add_category_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"products_add_category_swipe:{remover + 10}"),
        )

    return keyboard


# Страницы позиций для добавления товаров
async def products_add_position_swipe_fp(remover, category_id):
    get_positions = await get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_positions):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = await get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(InlineKeyboardButton(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"products_add_position_open:{get_positions[a]['position_id']}:{category_id}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"products_add_position_swipe:{category_id}:{remover + 10}")
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"products_add_position_swipe:{category_id}:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_positions) / 10)} 🔸", callback_data="...")
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"products_add_position_swipe:{category_id}:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"products_add_position_swipe:{category_id}:{remover + 10}"),
        )
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩", callback_data="products_add_category_swipe:0"))

    return keyboard


"Покупки товаров"


# Страницы категорий при покупке товара
async def products_item_category_swipe_fp(remover):
    get_categories = await get_all_categoriesx()
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.add(InlineKeyboardButton(get_categories[a]['category_name'],
                                              callback_data=f"buy_category_open:{get_categories[a]['category_id']}:0"))

    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_categories) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
        )
    elif remover + 10 >= len(get_categories):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸",
                                 callback_data="..."),
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"buy_category_swipe:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_categories) / 10)} 🔸",
                                 callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"buy_category_swipe:{remover + 10}"),
        )

    return keyboard


# Страницы позиций для покупки товаров
async def products_item_position_swipe_fp(remover, category_id):
    get_positions = await get_positionsx(category_id=category_id)
    keyboard = InlineKeyboardMarkup()

    if remover >= len(get_positions):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = await get_itemsx(position_id=get_positions[a]['position_id'])
            keyboard.add(InlineKeyboardButton(
                f"{get_positions[a]['position_name']} | {get_positions[a]['position_price']}₽ | {len(get_items)} шт",
                callback_data=f"buy_position_open:{get_positions[a]['position_id']}:{category_id}:{remover}"))

    if len(get_positions) <= 10:
        pass
    elif len(get_positions) > 10 and remover < 10:
        keyboard.add(
            InlineKeyboardButton(f"🔸 1/{ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}"),
        )
    elif remover + 10 >= len(get_positions):
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
        )
    else:
        keyboard.add(
            InlineKeyboardButton("⬅ Назад", callback_data=f"buy_position_swipe:{category_id}:{remover - 10}"),
            InlineKeyboardButton(f"🔸 {str(remover + 10)[:-1]}/{ceil(len(get_positions) / 10)} 🔸", callback_data="..."),
            InlineKeyboardButton("Далее ➡", callback_data=f"buy_position_swipe:{category_id}:{remover + 10}"),
        )
    keyboard.add(InlineKeyboardButton("⬅ Вернуться ↩", callback_data=f"buy_category_swipe:0"))

    return keyboard
