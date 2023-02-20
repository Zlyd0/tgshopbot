from aiogram.types import Update

from tgbot.database.methods.category import get_categoryx, get_all_categoriesx
from tgbot.database.methods.position import get_positionx, get_positionsx
from tgbot.keyboards.inline_page import products_item_category_swipe_fp, products_item_position_swipe_fp
from tgbot.loader import dp
from tgbot.utils.notify_admins import send_admins


# Обработка телеграм ошибок
@dp.errors_handler()
async def main_errors(update: Update, exception):
    get_data = None

    if "'NoneType' object is not subscriptable" in str(exception):
        if "callback_query" in update:
            get_data = update.callback_query.data

    if get_data is not None:
        split_data = get_data.split(":")

        if split_data[0] in ['buy_category_open']:
            get_category = await get_categoryx(category_id=split_data[1])

            if get_category is None:
                get_categories = await get_all_categoriesx()

                if len(get_categories) >= 1:
                    await update.callback_query.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                                                  reply_markup=await products_item_category_swipe_fp(0))
                    await update.callback_query.answer("❗ Категория была изменена или удалена")
                else:
                    await update.callback_query.message.edit_text("<b>🎁 Увы, товары в данное время отсутствуют.</b>")
                    await update.callback_query.answer("❗ Категория была изменена или удалена")
        elif split_data[0] in ['buy_position_open']:
            get_position = await get_positionx(position_id=split_data[1])

            if get_position is None:
                get_positions = await get_positionsx(category_id=split_data[3])

                if len(get_positions) >= 1:
                    await update.callback_query.message.edit_text("<b>🎁 Выберите нужный вам товар:</b>",
                                                                  reply_markup=await products_item_position_swipe_fp(
                                                                      int(split_data[2]), split_data[3]))
                    await update.callback_query.answer("❗ Позиция была изменена или удалена")
                else:
                    await update.callback_query.message.edit_text("<b>🎁 Увы, товары в данное время отсутствуют.</b>")
                    await update.callback_query.answer("❗ Позиция была изменена или удалена")
        elif split_data[0] in ['buy_item_open']:
            get_position = get_positionx(position_id=split_data[1])

            if get_position is None:
                await update.callback_query.message.edit_text("<b>🎁 Увы, товары в данное время отсутствуют.</b>")
                await update.callback_query.answer("❗ Позиция была изменена или удалена")

    # Логирование ошибок в ЛС бота
    await send_admins(f"<b>❌ Ошибка\n\n"
                      f"Exception: <code>{exception}</code>\n\n"
                      f"Update: <code>{update}</code></b>")
