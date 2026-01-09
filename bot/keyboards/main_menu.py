from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from bot.utils.texts import BotTexts

def get_main_menu_keyboard(user_id: int = None) -> InlineKeyboardMarkup:
    """Get enhanced main menu keyboard with better navigation"""
    keyboard = [
        # Main functions - simplified
        [
            InlineKeyboardButton(BotTexts.MY_LESSONS, callback_data="lessons")
        ],
        # Mini App - using direct web_app parameter
        [
            InlineKeyboardButton("🌐 Nomoz.uz", web_app={"url": f"https://www.nomoz.uz/{user_id}"})
        ] if user_id else []
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_reply_keyboard(user_id: int = None) -> ReplyKeyboardMarkup:
    """Get main menu reply keyboard (attached to keyboard)"""
    keyboard = [
        [KeyboardButton(BotTexts.MY_LESSONS)],
        [KeyboardButton("🌐 Nomoz.uz", web_app=WebAppInfo(url=f"https://www.nomoz.uz/{user_id}"))] if user_id else []
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard with back to main menu button"""
    keyboard = [
        [InlineKeyboardButton(BotTexts.MAIN_MENU, callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quick_actions_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for quick actions"""
    keyboard = [
        [InlineKeyboardButton(BotTexts.LATEST_RESULTS, callback_data="latest_results")],
        [InlineKeyboardButton(BotTexts.REFRESH, callback_data="refresh_data")],
        [InlineKeyboardButton(BotTexts.MAIN_MENU, callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Get settings menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔔 Bildirishnomalar", callback_data="notifications")],
        [InlineKeyboardButton("🌐 Til", callback_data="language")],
        [InlineKeyboardButton(BotTexts.MAIN_MENU, callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)