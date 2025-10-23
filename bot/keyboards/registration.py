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

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Get main menu keyboard after registration"""
    keyboard = [
        [InlineKeyboardButton(BotTexts.MY_LESSONS, callback_data="lessons")],
        [InlineKeyboardButton(BotTexts.MY_RESULTS, callback_data="results")]
    ]
    return InlineKeyboardMarkup(keyboard)