from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.texts import BotTexts

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Get main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(BotTexts.MY_LESSONS, callback_data="lessons")],
        [InlineKeyboardButton(BotTexts.MY_RESULTS, callback_data="results")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard with back to main menu button"""
    keyboard = [
        [InlineKeyboardButton(BotTexts.MAIN_MENU, callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)