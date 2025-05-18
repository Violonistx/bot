import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from config import BOT_TOKEN
from states import BookingStates
from handlers import start, afisha, booking, info, support
from utils import MASTER_CLASSES

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("booking", booking.start_booking),
            MessageHandler(filters.Regex("Забронировать"), booking.start_booking),
            CallbackQueryHandler(booking.start_booking, pattern=r"^book_event_\d+$")
        ],
        states={
            BookingStates.SELECT_EVENT: [
                CallbackQueryHandler(booking.select_event, pattern=r"^select_event_\d+$")
            ],
            BookingStates.NAME: [
                MessageHandler(filters.ALL, booking.get_name)
            ],
            BookingStates.PHONE: [
                MessageHandler(filters.ALL, booking.get_phone)
            ],
        },
        fallbacks=[CommandHandler("cancel", booking.cancel_booking)],
        per_user=True,
        per_chat=True,
        per_message=True
    )
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex("Афиша"), afisha.show_afisha))
    application.add_handler(MessageHandler(filters.Regex("Забронировать"), booking.start_booking))
    application.add_handler(MessageHandler(filters.Regex("О студии"), info.show_info))
    application.add_handler(MessageHandler(filters.Regex("Провести событие"), support.show_support))
    application.add_handler(MessageHandler(filters.Regex("Поддержка"), support.show_support))
    application.run_polling()

if __name__ == '__main__':
    main()