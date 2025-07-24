import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from db import save_message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не знайдено! Переконайся, що секрет встановлений у Fly.io")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())


@dp.message()
async def handle_message(message: types.Message):
    if message.chat.type in ["group", "supergroup"] and message.text:
        print(f"✅ Отримано повідомлення: {message.text}")
        await save_message(message)


async def main():
    print("🚀 Бот стартує...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
