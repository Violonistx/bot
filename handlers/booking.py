import logging
import re
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from states import BookingStates
from utils import MASTER_CLASSES, format_datetime

logger = logging.getLogger(__name__)

async def start_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data.clear()
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            event_id = int(query.data.split('_')[-1])
            selected_event = next((event for event in MASTER_CLASSES if event['id'] == event_id), None)
            if not selected_event:
                await query.message.reply_text("Извините, этот мастер-класс больше не доступен.")
                return ConversationHandler.END
            context.user_data["selected_event"] = selected_event
            event_time = format_datetime(selected_event['events'][0]['start_datetime'])
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=(
                    f"Вы выбрали мастер-класс: *{selected_event['name']}*\n"
                    f"💰 Цена: {selected_event['price']['final_price']}₽\n"
                    f"📍 Место: {selected_event['location']}\n"
                    f"🕒 Дата и время: {event_time}\n\n"
                    "Как вас зовут?"
                ),
                parse_mode="Markdown"
            )
            return BookingStates.NAME
        keyboard = []
        for i, event in enumerate(MASTER_CLASSES):
            keyboard.append([
                InlineKeyboardButton(
                    f"{event['name']} — {event['price']['final_price']}₽",
                    callback_data=f"select_event_{i}"
                )
            ])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Добро пожаловать в систему бронирования! 🎯\n\n"
            "Выберите мастер-класс, на который хотите записаться:",
            reply_markup=reply_markup
        )
        return BookingStates.SELECT_EVENT
    except Exception as e:
        logger.error(f"Error in start_booking: {e}")
        await update.message.reply_text("Произошла ошибка при начале бронирования. Пожалуйста, попробуйте позже.")
        return ConversationHandler.END

async def select_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        query = update.callback_query
        await query.answer()
        event_index = int(query.data.split('_')[-1])
        selected_event = MASTER_CLASSES[event_index]
        context.user_data["selected_event"] = selected_event
        await query.edit_message_text(
            f"Вы выбрали: *{selected_event['name']}*\n"
            f"Цена: {selected_event['price']['final_price']}₽\n"
            f"Место: {selected_event['location']}\n\n"
            "Как вас зовут?",
            parse_mode="Markdown"
        )
        return BookingStates.NAME
    except Exception as e:
        logger.error(f"Error in select_event: {e}")
        await update.callback_query.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        return ConversationHandler.END

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"get_name called. update.message: {update.message}")
    try:
        name = update.message.text.strip()
        if not name or len(name) < 2:
            await update.message.reply_text("Пожалуйста, введите корректное имя (минимум 2 символа).")
            return BookingStates.NAME
        context.user_data["name"] = name
        await update.message.reply_text("Укажите номер телефона в формате +7XXXXXXXXXX:")
        return BookingStates.PHONE
    except Exception as e:
        logger.error(f"Error in get_name: {e}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        return BookingStates.NAME

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        phone = update.message.text.strip()
        phone_pattern = re.compile(r'^\+?[78][\-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$')
        if not phone_pattern.match(phone):
            await update.message.reply_text("Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX")
            return BookingStates.PHONE
        context.user_data["phone"] = phone
        selected_event = context.user_data["selected_event"]
        event_time = format_datetime(selected_event['events'][0]['start_datetime'])
        context.user_data["time"] = event_time
        await update.message.reply_text(
            f"✅ Заявка получена!\n\n"
            f"Мастер-класс: {selected_event['name']}\n"
            f"Имя: {context.user_data['name']}\n"
            f"Телефон: {phone}\n"
            f"Время: {event_time}\n\n"
            f"Наш менеджер свяжется с вами в ближайшее время."
        )
        booking_data = {
            "event": selected_event,
            "name": context.user_data["name"],
            "phone": phone,
            "time": event_time,
            "booking_time": datetime.now().isoformat()
        }
        try:
            with open("bookings.json", "r", encoding="utf-8") as file:
                bookings = json.load(file)
            bookings["bookings"].append(booking_data)
            with open("bookings.json", "w", encoding="utf-8") as file:
                json.dump(bookings, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving booking: {e}")
        context.user_data.clear()
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in get_phone: {e}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        return BookingStates.PHONE

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        time_str = update.message.text.strip()
        try:
            booking_time = datetime.strptime(time_str, "%d.%m.%Y %H:%M")
            if booking_time < datetime.now():
                await update.message.reply_text("Пожалуйста, укажите будущую дату и время.")
                return BookingStates.TIME
        except ValueError:
            await update.message.reply_text("Пожалуйста, укажите дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ")
            return BookingStates.TIME
        booking_data = {
            "event": context.user_data["selected_event"],
            "name": context.user_data["name"],
            "phone": context.user_data["phone"],
            "time": time_str,
            "booking_time": datetime.now().isoformat()
        }
        try:
            with open("bookings.json", "r", encoding="utf-8") as file:
                bookings = json.load(file)
            bookings["bookings"].append(booking_data)
            with open("bookings.json", "w", encoding="utf-8") as file:
                json.dump(bookings, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving booking: {e}")
        await update.message.reply_text(
            f"✅ Заявка получена!\n\n"
            f"Мастер-класс: {context.user_data['selected_event']['name']}\n"
            f"Имя: {context.user_data['name']}\n"
            f"Телефон: {context.user_data['phone']}\n"
            f"Время: {time_str}\n\n"
            f"Наш менеджер свяжется с вами в ближайшее время."
        )
        context.user_data.clear()
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in get_time: {e}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
        return BookingStates.TIME

async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data.clear()
        await update.message.reply_text(
            "Бронирование отменено. Если у вас возникли вопросы, "
            "пожалуйста, обратитесь в поддержку.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in cancel_booking: {e}")
        await update.message.reply_text(
            "Произошла ошибка при отмене бронирования. "
            "Пожалуйста, попробуйте позже."
        )
        return ConversationHandler.END