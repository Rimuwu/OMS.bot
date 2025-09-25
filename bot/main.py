import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart


logging.basicConfig(level=logging.INFO)


BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())