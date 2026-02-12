from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

# вставь свой ключ OpenAI
client = OpenAI(api_key="OPENAI_KEY")

# вставь токен бота Telegram
BOT_TOKEN = "TELEGRAM_TOKEN"


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Ты дружелюбный помощник"},
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.choices[0].message.content

    await update.message.reply_text(answer)


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))

print("Бот запущен...")
app.run_polling()
