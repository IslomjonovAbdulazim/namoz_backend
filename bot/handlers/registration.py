import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from bot.services.user_service import UserService
from bot.utils.texts import BotTexts
from bot.keyboards.registration import get_phone_sharing_keyboard
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.utils.helpers import get_user_display_name

logger = logging.getLogger(__name__)

class RegistrationHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def handle_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle phone number sharing"""
        user = update.effective_user
        contact = update.message.contact
        
        if not contact or contact.user_id != user.id:
            await update.message.reply_text(
                BotTexts.PHONE_ERROR,
                reply_markup=get_phone_sharing_keyboard()
            )
            return
        
        try:
            # Register user with phone number
            success = await self.user_service.register_user(user, contact.phone_number)
            
            if success:
                await update.message.reply_text(
                    BotTexts.PHONE_RECEIVED,
                    reply_markup=ReplyKeyboardRemove()
                )
                
                # Show main menu
                welcome_text = BotTexts.WELCOME_REGISTERED.format(name=get_user_display_name(user))
                await update.message.reply_text(
                    welcome_text,
                    reply_markup=get_main_menu_keyboard(user.id),
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    BotTexts.PHONE_ERROR,
                    reply_markup=get_phone_sharing_keyboard()
                )
                
        except Exception as e:
            logger.error(f"Error handling contact from user {user.id}: {e}")
            await update.message.reply_text(
                BotTexts.GENERAL_ERROR,
                reply_markup=get_phone_sharing_keyboard()
            )
    
    async def request_phone_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Request phone number from new user"""
        await update.message.reply_text(
            BotTexts.PHONE_REQUEST,
            reply_markup=get_phone_sharing_keyboard()
        )