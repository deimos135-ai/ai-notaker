import os
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from openai import OpenAI
from db import save_message, get_weekly_messages

# 🔐 Токени
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 📄 Логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🤖 Ініціалізація бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# 🤖 Ініціалізація клієнта OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# ▶️ /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("👋 Привіт! Я бот для нотаток і підсумків. Напиши щось або надішли /summary")


# 📋 /summary
@dp.message(Command("summary"))
async def summary_handler(message: Message):
    logger.info(f"Запит /summary у чаті {message.chat.id}")
    try:
        recent = get_weekly_messages(chat_id=message.chat.id)
        if not recent:
            await message.answer("📭 Немає збережених повідомлень для резюме.")
            return

        text_block = "\n".join([f"{u or 'Користувач'}: {t}" for u, t, _ in recent if t])
        prompt = (
            "Зроби коротке та зрозуміле резюме цих повідомлень українською мовою:\n\n"
            + text_block
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )

        summary = response.choices[0].message.content.strip()
        await message.answer(f"📋 <b>Summary:</b>\n{summary}")
    except Exception as e:
        logger.error(f"❌ Помилка в summary_handler: {e}")
        await message.answer("❌ Помилка при створенні резюме.")


# 📨 Обробка повідомлень
@dp.message(F.text)
async def handle_message(message: Message):
    logger.info(f"✅ Отримано повідомлення: {message.text}")

    # Зберігаємо в SQLite
    save_message(
        chat_id=message.chat.id,
        username=message.from_user.username if message.from_user else "невідомо",
        text=message.text,
        timestamp=datetime.utcnow().isoformat()
    )

    # ⛔️ Не відповідає, щоб уникнути “папуги”


# 🚀 Запуск бота
async def main():
    logger.info("🚀 Бот стартує...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
