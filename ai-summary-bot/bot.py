import os
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot and Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Handlers
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("✅ Бот активний. Надсилай повідомлення.")

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def handle_group_message(message: Message):
    logger.info(f"✅ Отримано повідомлення: {message.text}")
    # TODO: Зберігати в базу / файл
    # Тут можна викликати функцію, яка логуватиме в CSV або SQLite

# Startup
async def on_startup(bot: Bot):
    logger.info("🚀 Бот стартує...")

# Shutdown
async def on_shutdown(bot: Bot):
    logger.info("🛑 Бот зупиняється...")

# Main
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
