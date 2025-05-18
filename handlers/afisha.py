from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import MASTER_CLASSES, format_datetime

logger = logging.getLogger(__name__)

async def show_afisha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not MASTER_CLASSES:
            await update.message.reply_text("Афиша пока пуста. Загляните позже!")
            return

        await update.message.reply_text(
            "🎨 *Ближайшие мастер-классы:*\n\n"
            "Выберите мастер-класс, чтобы узнать подробности или записаться:",
            parse_mode="Markdown"
        )

        for event in MASTER_CLASSES:
            try:
                keyboard = [[
                    InlineKeyboardButton(
                        "📝 Записаться",
                        callback_data=f"book_event_{event['id']}"
                    )
                ]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                event_time = format_datetime(event['events'][0]['start_datetime'])
                description = (
                    f"*{event['name']}*\n"
                    f"💰 Цена: {event['price']['final_price']}₽\n"
                    f"📍 Место: {event['location']}\n"
                    f"🕒 Дата и время: {event_time}\n\n"
                )

                if 'parameters' in event and 'parameters' in event['parameters']:
                    params = event['parameters']['parameters']
                    if 'Продолжительность' in params:
                        description += f"⏱ Продолжительность: {params['Продолжительность'][0]}\n"
                    if 'Возраст' in params:
                        description += f"👥 Возраст: {params['Возраст'][0]}\n"
                    if 'Количество участников' in params:
                        description += f"👥 Мест: {params['Количество участников'][0]}\n"


                if event['details']:
                    description += "\n" + "\n".join(event['details'])


                await update.message.reply_text(
                    description,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )

            except Exception as e:
                logger.error(f"Error processing event {event.get('id', 'unknown')}: {e}")
                continue

    except Exception as e:
        logger.error(f"Error in show_afisha: {e}")
        await update.message.reply_text(
            "Произошла ошибка при загрузке афиши. Пожалуйста, попробуйте позже."
        )