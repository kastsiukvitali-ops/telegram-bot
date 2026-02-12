import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    await update.message.reply_text(response.choices[0].message.content)


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot started...")
app.run_polling()
