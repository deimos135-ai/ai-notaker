import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен з ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Налаштування Bot
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher
dp = Dispatcher()

@dp.message(F.text)
async def echo_handler(message: Message):
    logger.info(f"✅ Отримано повідомлення: {message.text}")
    await message.answer("✅ Я працюю! Ви написали: " + message.text)

async def main():
    logger.info("🚀 Бот стартує...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
