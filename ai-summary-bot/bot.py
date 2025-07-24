import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import asyncio

# Зберігаємо повідомлення
weekly_messages = []

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токени з середовища
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація бота
bot = Bot(token=BOT_TOKEN, default=types.DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Функція для збереження повідомлення
def save_message(message: Message):
    weekly_messages.append((message.from_user.full_name, message.text, datetime.now()))

# Фільтр текстових повідомлень
@dp.message(F.text)
async def handle_message(message: Message):
    if message.chat.type in ["group", "supergroup"]:
        save_message(message)
        logger.info(f"✅ Отримано повідомлення: {message.text}")

# Команда для ручного виклику /summary
@dp.message(commands=["summary"])
async def send_summary(message: Message):
    await message.answer(generate_summary())

# Генерація підсумку
def generate_summary():
    if not weekly_messages:
        return "🔕 Немає повідомлень за останній тиждень."

    summary_lines = [f"<b>{name}:</b> {text}" for name, text, _ in weekly_messages]
    return "<b>🗓 Підсумок за тиждень:</b>\n\n" + "\n".join(summary_lines)

# Очистка старих повідомлень
def clear_old_messages():
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    global weekly_messages
    weekly_messages = [(u, t, ts) for u, t, ts in weekly_messages if ts >= week_ago]

# Автоматичний підсумок щоп’ятниці о 18:00
def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        auto_send_summary,
        trigger="cron",
        day_of_week="fri",
        hour=18,
        minute=0,
        timezone="Europe/Kyiv"
    )
    scheduler.start()

async def auto_send_summary():
    if not weekly_messages:
        return

    summary = generate_summary()

    # Надсилаємо підсумок у всі унікальні групи, які зберігали повідомлення
    unique_chats = set()
    for _, _, timestamp in weekly_messages:
        # При потребі додати збереження chat_id до weekly_messages
        pass

    # Або просто надсилай в одну тестову групу:
    test_chat_id = os.getenv("TEST_CHAT_ID")
    if test_chat_id:
        await bot.send_message(chat_id=test_chat_id, text=summary)

    clear_old_messages()

# Головна функція
async def main():
    logger.info("🚀 Бот стартує...")
    setup_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
