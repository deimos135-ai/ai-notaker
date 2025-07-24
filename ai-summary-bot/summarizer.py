import openai
import os
from db import get_messages_last_week

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_summary():
    messages = await get_messages_last_week()
    if not messages:
        return "Цього тижня не зафіксовано активностей у групах."

    text = "\n".join([f"{m['user']}: {m['text']}" for m in messages])
    prompt = f"""
Ти корпоративний асистент. Зроби короткий звіт про обговорення цього тижня у команді. Покажи основні теми, ключові рішення, важливі події. Ігноруй дрібниці, фокусуся на суті.

Ось повідомлення:
{text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response['choices'][0]['message']['content']
