import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from keyboards import main_keyboard

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        context.user_data.clear()
        await update.message.reply_text(
            "👋 Добро пожаловать в студию мастер-классов Les Jour!\n\n"
            "Я помогу вам:\n"
            "📅 Узнать о предстоящих мастер-классах\n"
            "📝 Забронировать место на мастер-класс\n"
            "🎉 Организовать свое событие\n\n"
            "Выберите нужный пункт в меню ниже:",
            reply_markup=main_keyboard
        )
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(
            "Произошла ошибка при запуске бота. Пожалуйста, попробуйте позже."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        help_text = (
            "🤖 *Справка по командам бота:*\n\n"
            "/start - Запустить бота и показать главное меню\n"
            "/help - Показать эту справку\n"
            "/cancel - Отменить текущее действие\n\n"
            "*Основные функции:*\n"
            "📅 Афиша - Посмотреть расписание мастер-классов\n"
            "📝 Забронировать - Записаться на мастер-класс\n"
            "🎉 Провести событие - Организовать свое мероприятие\n"
            "🏢 О студии - Узнать больше о нашей студии\n"
            "📞 Поддержка - Связаться с нами\n\n"
            "Если у вас возникли вопросы, используйте кнопку 'Поддержка' "
            "или напишите нам напрямую."
        )
        await update.message.reply_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=main_keyboard
        )
    except Exception as e:
        logger.error(f"Error in help command: {e}")
        await update.message.reply_text(
            "Произошла ошибка при показе справки. Пожалуйста, попробуйте позже."
        )