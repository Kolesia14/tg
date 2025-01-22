from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging

# Токен вашего бота
BOT_TOKEN = "7704656534:AAHHSxnfIrmnuWYDrYGS9DuWd-hnNcsC14I"

# Список админов
ADMINS = ["356538599"]  # Укажите ваш Telegram ID как строку или число

# Логирование
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Кнопки для админа
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(KeyboardButton("Добавить позицию"))
admin_keyboard.add(KeyboardButton("Удалить позицию"))
admin_keyboard.add(KeyboardButton("Изменить количество"))

# Хранилище данных
positions = {
    "Сталь": [],
    "09г2с": []
}


# Команда /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.reply("Добро пожаловать, Админ! Выберите действие:", reply_markup=admin_keyboard)
    else:
        await message.reply("Вы Гость! У вас только права просмотра.")


# Обработка кнопки "Добавить позицию"
@dp.message_handler(lambda message: message.text == "Добавить позицию")
async def add_position(message: types.Message):
    await message.reply("Введите данные для новой позиции в формате: 'Марка_стали: Толщина (Размер) - Количество'\n"
                        "Например: 'Сталь: 5мм (1250×6000мм) - 10шт'")


# Обработка добавления новой позиции
@dp.message_handler(lambda message: ":" in message.text and "-" in message.text)
async def process_add_position(message: types.Message):
    try:
        # Пример: "Сталь: 5мм (1250×6000мм) - 10шт"
        data = message.text.split(":")
        category = data[0].strip()  # "Сталь" или "09г2с"
        position = data[1].strip()  # "5мм (1250×6000мм) - 10шт"

        if category not in positions:
            await message.reply("Ошибка: Неверная марка стали. Используйте 'Сталь' или '09г2с'.")
            return

        positions[category].append(position)
        await message.reply(f"Позиция добавлена в раздел {category}: {position}")
    except Exception as e:
        await message.reply(f"Ошибка обработки данных: {e}")


# Обработка кнопки "Удалить позицию"
@dp.message_handler(lambda message: message.text == "Удалить позицию")
async def delete_position(message: types.Message):
    await message.reply("Введите позицию, которую нужно удалить, в формате: 'Марка_стали: Позиция'\n"
                        "Например: 'Сталь: 5мм (1250×6000мм)'")

# Удаление позиции
@dp.message_handler(lambda message: ":" in message.text and message.text.startswith(("Сталь", "09г2с")))
async def process_delete_position(message: types.Message):
    try:
        data = message.text.split(":")
        category = data[0].strip()  # "Сталь" или "09г2с"
        position = data[1].strip()  # "5мм (1250×6000мм)"

        if category not in positions:
            await message.reply("Ошибка: Неверная марка стали. Используйте 'Сталь' или '09г2с'.")
            return

        if position in positions[category]:
            positions[category].remove(position)
            await message.reply(f"Позиция удалена из раздела {category}: {position}")
        else:
            await message.reply(f"Позиция не найдена в разделе {category}.")
    except Exception as e:
        await message.reply(f"Ошибка обработки данных: {e}")


# Обработка кнопки "Изменить количество"
@dp.message_handler(lambda message: message.text == "Изменить количество")
async def edit_quantity(message: types.Message):
    await message.reply("Введите данные для изменения количества в формате: 'Марка_стали: Позиция - Новое_количество'\n"
                        "Например: 'Сталь: 5мм (1250×6000мм) - 15шт'")


# Изменение количества
@dp.message_handler(lambda message: ":" in message.text and "-" in message.text)
async def process_edit_quantity(message: types.Message):
    try:
        data = message.text.split(":")
        category = data[0].strip()  # "Сталь" или "09г2с"
        position_data = data[1].strip().split("-")
        position = position_data[0].strip()  # "5мм (1250×6000мм)"
        new_quantity = position_data[1].strip()  # "15шт"

        if category not in positions:
            await message.reply("Ошибка: Неверная марка стали. Используйте 'Сталь' или '09г2с'.")
            return

        for i, pos in enumerate(positions[category]):
            if pos.startswith(position):
                positions[category][i] = f"{position} - {new_quantity}"
                await message.reply(f"Количество обновлено для позиции {position}: {new_quantity}")
                return

        await message.reply(f"Позиция {position} не найдена в разделе {category}.")
    except Exception as e:
        await message.reply(f"Ошибка обработки данных: {e}")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)