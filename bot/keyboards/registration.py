from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.texts import BotTexts

def get_phone_sharing_keyboard() -> ReplyKeyboardMarkup:
    """Get keyboard for phone number sharing"""
    keyboard = [
        [KeyboardButton("📱 Telefon raqamini baham ko'rish", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Telefon raqamingizni baham ko'ring"
    )

