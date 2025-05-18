import logging
import re
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from states import EventStates

logger = logging.getLogger(__name__)

async def start_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data.clear()
        await update.message.reply_text(
            "Добро пожаловать в систему организации событий! 🎉\n\n"
            "Для отмены заявки в любой момент используйте команду /cancel\n\n"
            "Как вас зовут?"
        )
        return EventStates.NAME
    except Exception as e:
        logger.error(f"Error in start_event: {e}")
        await update.message.reply_text(
            "Произошла ошибка при начале оформления заявки. Пожалуйста, попробуйте позже."
        )
        return ConversationHandler.END

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        name = update.message.text.strip()
        if not name or len(name) < 2:
            await update.message.reply_text(
                "Пожалуйста, введите корректное имя (минимум 2 символа)."
            )
            return EventStates.NAME
        context.user_data["name"] = name
        await update.message.reply_text(
            "Укажите номер телефона в формате +7XXXXXXXXXX:"
        )
        return EventStates.PHONE
    except Exception as e:
        logger.error(f"Error in get_name: {e}")
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте еще раз."
        )
        return EventStates.NAME

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        phone = update.message.text.strip()
        phone_pattern = re.compile(r'^\+?[78][\-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$')
        if not phone_pattern.match(phone):
            await update.message.reply_text(
                "Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX"
            )
            return EventStates.PHONE
        context.user_data["phone"] = phone
        await update.message.reply_text(
            "Коротко опишите, какое событие вы хотите организовать:\n"
            "- Тип события\n"
            "- Примерное количество гостей\n"
            "- Желаемая дата\n"
            "- Особые пожелания"
        )
        return EventStates.COMMENT
    except Exception as e:
        logger.error(f"Error in get_phone: {e}")
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте еще раз."
        )
        return EventStates.PHONE

async def get_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        comment = update.message.text.strip()
        if not comment or len(comment) < 10:
            await update.message.reply_text(
                "Пожалуйста, предоставьте более подробное описание события "
                "(минимум 10 символов)."
            )
            return EventStates.COMMENT
        context.user_data["comment"] = comment
        name = context.user_data["name"]
        phone = context.user_data["phone"]
        await update.message.reply_text(
            f"✅ Заявка принята!\n\n"
            f"📋 Детали заявки:\n"
            f"👤 Имя: {name}\n"
            f"📱 Телефон: {phone}\n"
            f"📝 Описание события:\n{comment}\n\n"
            f"Мы свяжемся с вами в ближайшее время для обсуждения деталей.\n"
            f"Спасибо за выбор нашей студии! 🎯"
        )
        context.user_data.clear()
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in get_comment: {e}")
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте еще раз."
        )
        return EventStates.COMMENT

async def cancel_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data.clear()
        await update.message.reply_text(
            "Заявка на организацию события отменена. Если у вас возникли вопросы, "
            "пожалуйста, обратитесь в поддержку.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in cancel_event: {e}")
        await update.message.reply_text(
            "Произошла ошибка при отмене заявки. "
            "Пожалуйста, попробуйте позже."
        )
        return ConversationHandler.END