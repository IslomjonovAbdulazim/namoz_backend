from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.texts import BotTexts

def get_main_menu_keyboard(user_id: int = None) -> InlineKeyboardMarkup:
    """Get enhanced main menu keyboard with better navigation"""
    keyboard = [
        # Main functions - two in a row for better layout
        [
            InlineKeyboardButton(BotTexts.MY_LESSONS, callback_data="lessons"),
            InlineKeyboardButton(BotTexts.MY_RESULTS, callback_data="results")
        ],
        # Quick actions
        [
            InlineKeyboardButton(BotTexts.QUICK_LESSONS, callback_data="quick_lessons"),
            InlineKeyboardButton(BotTexts.PROGRESS, callback_data="progress")
        ],
        # Profile and help
        [
            InlineKeyboardButton(BotTexts.PROFILE, callback_data="profile"),
            InlineKeyboardButton(BotTexts.HELP, callback_data="help")
        ],
        # Mini App - using direct web_app parameter
        [
            InlineKeyboardButton("🌐 Nomoz.uz", web_app={"url": f"https://www.nomoz.uz/{user_id}"})
        ] if user_id else []
    ]
    return InlineKeyboardMarkup(keyboard)

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