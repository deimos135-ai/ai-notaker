import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram import F

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не встановлено в оточенні")

# Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Start command from chat_id: {message.chat.id}")
    await message.answer("👋 Привіт! Я бот і вже працюю!")

@dp.message(Command("summary"))
async def summary_handler(message: Message):
    logger.info(f"Summary запит від chat_id: {message.chat.id}")
    await message.answer("📝 Тут буде summary. Але наразі ця функція ще в розробці.")

# Якщо хочеш реакцію на інші повідомлення — розкоментуй
# @dp.message(F.text)
# async def echo_handler(message: Message):
#     logger.info(f"Echo від chat_id: {message.chat.id} — {message.text}")
#     await message.answer(f"✅ Ви написали: {message.text}")

async def main():
    logger.info("🚀 Бот стартує...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
