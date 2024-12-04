import os  # Вернули импорт os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import handle_photo, handle_voice_message, handle_translation
from dotenv import load_dotenv
from aiogram import F

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # Хранилище для состояний (FSM, если нужно)
dp = Dispatcher(storage=storage)

# Клавиатура
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сохранить фото")],
        [KeyboardButton(text="Голосовое сообщение")],
        [KeyboardButton(text="Перевести")]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start_command(message: Message):
    """Обработка команды /start и отображение меню."""
    await message.answer("Выберите действие из меню:", reply_markup=menu_keyboard)


@dp.message(F.text == "Сохранить фото")
async def save_photo_handler(message: Message):
    """Реакция на нажатие кнопки 'Сохранить фото'."""
    await message.answer("Отправьте фото, чтобы сохранить его.")


@dp.message(F.photo)
async def photo_handler(message: Message):
    """Сохраняет фотографию, отправленную пользователем."""
    await handle_photo(message)


@dp.message(F.text == "Голосовое сообщение")
async def voice_message_handler(message: Message):
    """Реакция на нажатие кнопки 'Голосовое сообщение'."""
    await handle_voice_message(bot, message.chat.id)


@dp.message(F.text == "Перевести")
async def translate_prompt(message: Message):
    """Реакция на нажатие кнопки 'Перевести'."""
    await message.answer("Отправьте текст для перевода на английский язык.")


@dp.message(F.text)
async def translation_handler(message: Message):
    """Переводит текст на английский язык, если он не совпадает с командами кнопок."""
    await handle_translation(message)


async def main():
    """Основной запуск бота."""
    await bot.delete_webhook(drop_pending_updates=True)  # Очистка вебхуков
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
