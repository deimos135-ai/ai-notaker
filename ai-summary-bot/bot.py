import os
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties

from db import save_message, get_weekly_messages
import openai

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ключі
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Бот
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("👋 Привіт! Я бот для нотаток і підсумків. Напиши щось або надішли /summary")


@dp.message(Command("summary"))
async def summary_handler(message: Message):
    logger.info(f"Запит /summary у чаті {message.chat.id}")

    try:
        messages = get_weekly_messages()
        chat_messages = [m for m in messages if str(message.chat.id) in str(m[0])]

        if not chat_messages:
            await message.answer("📭 Немає збережених повідомлень для резюме.")
            return

        text_block = "\n".join([f"{m[1]}" for m in chat_messages if m[1]])
        prompt = (
            "Зроби коротке та зрозуміле резюме цих повідомлень українською мовою:\n\n"
            + text_block
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        summary = response.choices[0].message.content.strip()
        await message.answer(f"📋 <b>Summary:</b>\n{summary}")
    except Exception as e:
        logger.error(f"Помилка в summary_handler: {e}")
        await message.answer("❌ Помилка при створенні резюме.")


@dp.message(F.text)
async def echo_and_store(message: Message):
    logger.info(f"✅ Отримано повідомлення: {message.text}")
    timestamp = datetime.utcnow().isoformat()
    save_message(
        chat_id=message.chat.id,
        username=message.from_user.username,
        text=message.text,
        timestamp=timestamp
    )
    await message.reply(message.text)


async def main():
    logger.info("🚀 Бот стартує...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
