import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.client.default import DefaultBotProperties
from sqlalchemy import select
from db import SessionLocal, MessageModel  # твоя SQLAlchemy модель
import openai

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ключі
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Ініціалізація бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# Збереження повідомлення у БД
def save_message_to_db(msg: Message):
    with SessionLocal() as session:
        db_msg = MessageModel(
            chat_id=msg.chat.id,
            user_id=msg.from_user.id if msg.from_user else None,
            username=msg.from_user.username if msg.from_user else None,
            text=msg.text
        )
        session.add(db_msg)
        session.commit()


# Витяг останніх повідомлень

def get_recent_messages(chat_id: int, limit: int = 20):
    with SessionLocal() as session:
        stmt = (
            select(MessageModel)
            .where(MessageModel.chat_id == chat_id)
            .order_by(MessageModel.timestamp.desc())
            .limit(limit)
        )
        return list(reversed(session.scalars(stmt).all()))


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("👋 Привіт! Я бот для нотаток і підсумків. Напиши щось або надішли /summary")


@dp.message(Command("summary"))
async def summary_handler(message: Message):
    logger.info(f"Запит /summary у чаті {message.chat.id}")

    try:
        recent = get_recent_messages(chat_id=message.chat.id, limit=20)
        if not recent:
            await message.answer("📭 Немає збережених повідомлень для резюме.")
            return

        text_block = "\n".join([msg.text for msg in recent if msg.text])
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
    save_message_to_db(message)
    await message.reply(message.text)


async def main():
    logger.info("🚀 Бот стартує...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

    import asyncio
    asyncio.run(main())
