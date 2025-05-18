from telegram import Update
from telegram.ext import ContextTypes

async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Мы — студия мастер-классов Les Jour.\n\nПроводим творческие мероприятия, гончарные и художественные занятия. "
        "Выездные корпоративы, индивидуальные занятия и детские праздники — всё в нашем репертуаре!"
    )