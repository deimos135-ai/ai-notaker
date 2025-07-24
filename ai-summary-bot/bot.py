import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import save_message, get_weekly_messages

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

@dp.message()
async def handle_message(message: Message):
    logger.info(f"✅ Отримано повідомлення: {message.text}")
    save_message(
        chat_id=message.chat.id,
        username=message.from_user.username or "невідомо",
        text=message.text,
        timestamp=message.date.isoformat()
    )

@scheduler.scheduled_job("cron", day_of_week="fri", hour=18)
async def weekly_summary():
    messages = get_weekly_messages()
    if not messages:
        return

    summary_text = "<b>🗓 Щотижневий підсумок:</b>\n\n"
    for username, text, timestamp in messages:
        summary_text += f"<b>{username}:</b> {text}\n"

    chat_id = messages[-1][0]  # або вкажи фіксований chat_id вручну
    await bot.send_message(chat_id=chat_id, text=summary_text)

async def main():
    logger.info("🚀 Бот стартує...")
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
