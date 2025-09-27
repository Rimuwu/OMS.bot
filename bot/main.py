import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from os import getenv
from dotenv import load_dotenv

from oms import register_handlers

load_dotenv()
logging.basicConfig(level=logging.INFO)

mainbot = Bot(token=getenv("BOT_TOKEN", ''))

dp = Dispatcher()

def run():
    import bot.handlers
    register_handlers(dp)
    
    print("Бот запущен")
    asyncio.run(dp.start_polling(mainbot))