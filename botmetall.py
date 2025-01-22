from config import ADMINS
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

API_TOKEN = "7704656534:AAHHSxnfIrmnuWYDrYGS9DuWd-hnNcsC14I"  # Вставьте токен вашего бота

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Начальные данные
data = {
    "Сталь": {
        "4мм (1250×2500мм)": 0,
        "4мм (1250×4000мм)": 0,
        "4мм (1500×6000мм)": 0,
        "5мм (1500×6000мм)": 0,
        "8мм (1500×6000мм)": 0,
        "10мм (1500×6000мм)": 0,
        "14мм (указать размер)": 0,
        "20мм (указать размер)": 0,
        "30мм (указать размер)": 0,
    },
    "09г2с": {
        "4мм (1500×6000мм)": 0,
        "5мм (1500×6000мм)": 0,
        "6мм (1500×6000мм)": 0,
        "8мм (1500×6000мм)": 0,
        "16мм (1500×4000мм)": 0,
        "16мм (1500×6000мм)": 0,
    }
}

# Роли пользователей
admins = [356538599]  # Здесь добавьте ID админов (например, [123456789])
guests = []  # Здесь добавьте ID гостей (например, [987654321])

# Кнопки главного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Сталь"), KeyboardButton("09г2с"))


# Формирование таблицы остатков
def format_table(section):
    table = f"Раздел: {section}\n"
    for position, quantity in data[section].items():
        table += f"{position} - {quantity} шт\n"
    return table


# Команда /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    role = "Гость"
    if message.from_user.id in admins:
        role = "Админ"
    elif message.from_user.id in guests:
        role = "Гость"

    greeting = f"Привет, {message.from_user.first_name}! Ваша роль: {role}.\nВыберите раздел для просмотра остатков:"
    await message.answer(greeting, reply_markup=main_menu)


# Обработка выбора раздела
@dp.message_handler(lambda message: message.text in data.keys())
async def show_section(message: types.Message):
    section = message.text
    table = format_table(section)
    await message.answer(table)


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    executor.start_polling(dp, skip_updates=True)