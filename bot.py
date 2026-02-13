import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# Логирование (чтобы видеть ошибки в Railway)
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет 👋 Напиши мне что-нибудь")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник."},
                {"role": "user", "content": user_text},
            ],
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        await update.message.reply_text("Ошибка при обращении к ИИ 😢")


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
