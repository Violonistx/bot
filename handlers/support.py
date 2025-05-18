from telegram import Update
from telegram.ext import ContextTypes

async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Поддержка: +7 900 000-00-00\n✉️ Email: hello@lesjour.ru\n\nПишите нам по любым вопросам!"
    )