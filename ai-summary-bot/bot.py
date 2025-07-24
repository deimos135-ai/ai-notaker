import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from db import save_message

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message()
async def handle_message(message: types.Message):
    if message.chat.type in ["group", "supergroup"] and message.text:
        await save_message(message)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
