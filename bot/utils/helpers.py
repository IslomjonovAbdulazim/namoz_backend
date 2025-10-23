import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

def format_date(date_str: str) -> str:
    """Format ISO date string to readable format"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d.%m.%Y')
    except:
        return date_str[:10] if len(date_str) >= 10 else date_str

def format_phone_number(phone: str) -> str:
    """Format phone number for display"""
    if phone.startswith('+'):
        return phone
    return f"+{phone}"

def truncate_text(text: str, max_length: int = 25) -> str:
    """Truncate text for button labels"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def calculate_correct_answers(score: int, total: int) -> int:
    """Calculate number of correct answers from percentage"""
    return (score * total) // 100

def is_valid_telegram_id(telegram_id: int) -> bool:
    """Check if telegram_id is valid"""
    return isinstance(telegram_id, int) and telegram_id > 0

def get_user_display_name(user) -> str:
    """Get display name for user"""
    if user.first_name and user.last_name:
        return f"{user.first_name} {user.last_name}"
    elif user.first_name:
        return user.first_name
    elif user.username:
        return f"@{user.username}"
    else:
        return "Foydalanuvchi"

def safe_int(value, default: int = 0) -> int:
    """Safely convert to int"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def log_user_action(user_id: int, action: str, details: str = ""):
    """Log user actions for debugging"""
    logger.info(f"User {user_id}: {action} {details}")

def format_price(price: int) -> str:
    """Format price with thousand separators"""
    return f"{price:,} so'm"