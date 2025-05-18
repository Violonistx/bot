import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

with open("data.json", "r", encoding="utf-8") as file:
    MASTER_CLASSES = json.load(file)

def format_datetime(dt_str):
    """Форматирует дату и время из ISO формата в читаемый вид."""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%d.%m.%Y %H:%M')
    except Exception as e:
        logger.error(f"Error formatting datetime {dt_str}: {e}")
        return dt_str 