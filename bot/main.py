import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота (замените на ваш токен)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Создание объектов бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Основная функция запуска бота
async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())