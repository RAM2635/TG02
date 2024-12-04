import os
from aiogram import Bot, Dispatcher, types
from googletrans import Translator
from aiogram.types import FSInputFile

# Инициализация переводчика
translator = Translator()

# Папка для сохранения изображений
IMAGE_FOLDER = "img"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


async def handle_photo(message: types.Message):
    """Сохраняет фото, отправленное пользователем."""
    IMAGE_FOLDER = os.path.join(os.getcwd(), "img")  # Путь к папке img
    os.makedirs(IMAGE_FOLDER, exist_ok=True)  # Создаём папку, если её нет

    # Берём самое большое фото
    photo = message.photo[-1]

    # Указываем имя файла для сохранения
    photo_path = os.path.join(IMAGE_FOLDER, f"{photo.file_id}.jpg")

    # Скачиваем файл с помощью метода bot.download
    await message.bot.download(photo.file_id, destination=photo_path)

    await message.answer("Фото сохранено!")

# Отправка голосового сообщения
async def handle_voice_message(bot: Bot, chat_id: int):
    """Отправляет голосовое сообщение в формате Telegram."""
    voice_path = os.path.join(os.path.dirname(__file__), "voice.ogg")

    # Проверяем, существует ли файл
    if not os.path.exists(voice_path):
        await bot.send_message(chat_id, "Голосовой файл не найден.")
        return

    # Создаём объект FSInputFile
    voice_file = FSInputFile(voice_path)

    # Отправляем голосовое сообщение с параметрами
    await bot.send_voice(
        chat_id=chat_id,
        voice=voice_file,
        duration=3,  # Укажите длительность голосового сообщения в секундах
        caption="Это тестовое голосовое сообщение",  # Текст под сообщением
    )

# Перевод текста
async def handle_translation(message: types.Message):
    """Переводит текст на английский язык."""
    from googletrans import Translator
    translator = Translator()
    translated_text = translator.translate(message.text, src="auto", dest="en").text
    await message.answer(f"Перевод: {translated_text}")
