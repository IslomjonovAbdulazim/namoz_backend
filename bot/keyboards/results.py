from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict, Any
from bot.utils.texts import BotTexts
from bot.utils.helpers import truncate_text

def get_results_list_keyboard(results: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Get keyboard for results list"""
    keyboard = []
    
    if results:
        for result in results:
            score_icon = BotTexts.get_score_icon(result["score"])
            button_text = f"{score_icon} {truncate_text(result['lesson_title'])} ({result['score']}%)"
            
            keyboard.append([InlineKeyboardButton(
                button_text,
                callback_data=f"result_detail_{result['id']}"
            )])
    
    # Control buttons
    keyboard.append([InlineKeyboardButton(BotTexts.BACK_TO_LESSONS, callback_data="lessons")])
    keyboard.append([InlineKeyboardButton(BotTexts.MAIN_MENU, callback_data="start")])
    
    return InlineKeyboardMarkup(keyboard)

def get_result_detail_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for result details"""
    keyboard = [
        [InlineKeyboardButton(BotTexts.BACK_TO_RESULTS, callback_data="results")]
    ]
    return InlineKeyboardMarkup(keyboard)