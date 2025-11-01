from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict, Any
from bot.utils.texts import BotTexts
from bot.utils.helpers import truncate_text

def get_lessons_list_keyboard(lessons: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Get keyboard for lessons list"""
    keyboard = []
    
    for lesson in lessons:
        status_icon = BotTexts.UNLOCKED_ICON if lesson["has_access"] else BotTexts.LOCKED_ICON
        button_text = f"{status_icon} {truncate_text(lesson['title'])}"
        
        keyboard.append([InlineKeyboardButton(
            button_text, 
            callback_data=f"lesson_{lesson['id']}"
        )])
    
    # Add control buttons
    keyboard.append([InlineKeyboardButton(BotTexts.REFRESH, callback_data="lessons")])
    keyboard.append([InlineKeyboardButton(BotTexts.MAIN_MENU, callback_data="start")])
    
    return InlineKeyboardMarkup(keyboard)

def get_lesson_detail_keyboard(lesson_id: str, has_access: bool, test_completed: bool = False) -> InlineKeyboardMarkup:
    """Get keyboard for lesson detail"""
    keyboard = []
    
    if has_access:
        # Add material buttons - these will be URLs
        # Note: URLs will be added dynamically based on lesson data
        
        # Add test button - always show test option
        keyboard.append([InlineKeyboardButton(BotTexts.TAKE_TEST, callback_data=f"test_{lesson_id}")])
    
    # Back button
    keyboard.append([InlineKeyboardButton(BotTexts.BACK_TO_LESSONS, callback_data="lessons")])
    
    return InlineKeyboardMarkup(keyboard)

def get_lesson_materials_keyboard(lesson_data: Dict[str, Any], lesson_id: str) -> InlineKeyboardMarkup:
    """Get keyboard with material URLs and test button"""
    keyboard = []
    
    # Add material buttons with URLs
    if lesson_data.get("video_url"):
        keyboard.append([InlineKeyboardButton(BotTexts.VIDEO, url=lesson_data["video_url"])])
    
    if lesson_data.get("pdf_url"):
        keyboard.append([InlineKeyboardButton(BotTexts.PDF, url=lesson_data["pdf_url"])])
    
    if lesson_data.get("ppt_url"):
        keyboard.append([InlineKeyboardButton(BotTexts.PRESENTATION, url=lesson_data["ppt_url"])])
    
    # Test button - always show test option
    keyboard.append([InlineKeyboardButton(BotTexts.TAKE_TEST, callback_data=f"test_{lesson_id}")])
    
    # Back button
    keyboard.append([InlineKeyboardButton(BotTexts.BACK_TO_LESSONS, callback_data="lessons")])
    
    return InlineKeyboardMarkup(keyboard)

def get_test_question_keyboard(question_id: str, options: List[str], lesson_id: str) -> InlineKeyboardMarkup:
    """Get keyboard for test question"""
    keyboard = []
    
    # Add option buttons
    for i, option in enumerate(options):
        letter = chr(65 + i)  # A, B, C, D
        # Try to avoid truncation by using a more generous limit
        # Telegram can handle reasonably long button text
        button_text = f"{letter}. {option}"
        
        keyboard.append([InlineKeyboardButton(
            button_text, 
            callback_data=f"answer_{question_id}_{i}"
        )])
    
    # Cancel test button
    keyboard.append([InlineKeyboardButton(BotTexts.CANCEL_TEST, callback_data=f"lesson_{lesson_id}")])
    
    return InlineKeyboardMarkup(keyboard)

def get_test_finished_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard after test completion"""
    keyboard = [
        [InlineKeyboardButton(BotTexts.BACK_TO_LESSONS, callback_data="lessons")],
        [InlineKeyboardButton(BotTexts.MY_RESULTS, callback_data="results")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_locked_lesson_keyboard(lesson_title: str = "", lesson_price: str = "") -> InlineKeyboardMarkup:
    """Get keyboard for locked lesson with contact admin button"""
    # Create pre-filled message with course details
    message = f"Salom! Men '{lesson_title}' darsini sotib olishni xohlayman."
    if lesson_price:
        message += f" Narxi: {lesson_price}"
    message += " Iltimos, to'lov va kirish haqida ma'lumot bering."
    
    # URL encode the message
    import urllib.parse
    encoded_message = urllib.parse.quote(message)
    contact_url = f"https://t.me/Ekolingvist1?text={encoded_message}"
    
    keyboard = [
        [InlineKeyboardButton("💳 Administrator bilan bog'lanish", url=contact_url)],
        [InlineKeyboardButton(BotTexts.BACK_TO_LESSONS, callback_data="lessons")]
    ]
    return InlineKeyboardMarkup(keyboard)