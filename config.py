import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен бота из переменных окружения
BOT_TOKEN = "7815643193:AAExrmaoLEBynnKfoD2RHwLjNmFSwFcicj0"

if not BOT_TOKEN:
    raise ValueError("Не найден токен бота. Убедитесь, что файл .env существует и содержит BOT_TOKEN")