from telegram import ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup([
    ["📅 Афиша", "📝 Забронировать"],
    ["🏢 О студии", "🎉 Провести событие"],
    ["📞 Поддержка"]
], resize_keyboard=True)