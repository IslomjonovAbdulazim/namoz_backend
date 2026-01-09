import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from bot.services.user_service import UserService
from bot.utils.texts import BotTexts
from bot.keyboards.main_menu import get_main_menu_keyboard, get_main_menu_reply_keyboard
from bot.keyboards.registration import get_phone_sharing_keyboard
from bot.utils.helpers import get_user_display_name
from bot.handlers.registration import RegistrationHandler

logger = logging.getLogger(__name__)

class CommandHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.registration_handler = RegistrationHandler(user_service)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        try:
            # Check if user is registered
            is_registered = await self.user_service.is_user_registered(user.id)
            
            if is_registered:
                # User is registered, show main menu
                welcome_text = BotTexts.WELCOME_REGISTERED.format(name=get_user_display_name(user))
                await update.message.reply_text(
                    welcome_text,
                    reply_markup=get_main_menu_reply_keyboard(user.id)
                )
                await update.message.reply_text(
                    "Quyidagi tugmalar orqali botdan foydalaning:",
                    reply_markup=get_main_menu_keyboard(user.id)
                )
            else:
                # User not registered, request phone number
                welcome_text = BotTexts.WELCOME.format(name=get_user_display_name(user))
                await update.message.reply_text(welcome_text)
                await self.registration_handler.request_phone_number(update, context)
                
        except Exception as e:
            logger.error(f"Error in start command for user {user.id}: {e}")
            await update.message.reply_text(BotTexts.GENERAL_ERROR)
    
    async def lessons_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /lessons command"""
        user = update.effective_user
        
        try:
            # Check if user is registered
            is_registered = await self.user_service.is_user_registered(user.id)
            
            if not is_registered:
                await self.registration_handler.request_phone_number(update, context)
                return
            
            # Import here to avoid circular import
            from bot.handlers.callbacks import CallbackHandler
            callback_handler = CallbackHandler(self.user_service)
            await callback_handler.show_lessons(update, context)
            
        except Exception as e:
            logger.error(f"Error in lessons command for user {user.id}: {e}")
            await update.message.reply_text(BotTexts.GENERAL_ERROR)
    
    async def results_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /results command"""
        user = update.effective_user
        
        try:
            # Check if user is registered
            is_registered = await self.user_service.is_user_registered(user.id)
            
            if not is_registered:
                await self.registration_handler.request_phone_number(update, context)
                return
            
            # Import here to avoid circular import
            from bot.handlers.callbacks import CallbackHandler
            callback_handler = CallbackHandler(self.user_service)
            await callback_handler.show_results(update, context)
            
        except Exception as e:
            logger.error(f"Error in results command for user {user.id}: {e}")
            await update.message.reply_text(BotTexts.GENERAL_ERROR)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        try:
            from bot.keyboards.main_menu import get_back_to_main_keyboard
            
            await update.message.reply_text(
                BotTexts.HELP_TEXT,
                reply_markup=get_back_to_main_keyboard(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await update.message.reply_text(BotTexts.GENERAL_ERROR)
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command"""
        user = update.effective_user
        
        try:
            # Check if user is registered
            is_registered = await self.user_service.is_user_registered(user.id)
            
            if not is_registered:
                await self.registration_handler.request_phone_number(update, context)
                return
            
            # Import here to avoid circular import
            from bot.handlers.callbacks import CallbackHandler
            callback_handler = CallbackHandler(self.user_service)
            await callback_handler.show_profile(update, context)
            
        except Exception as e:
            logger.error(f"Error in profile command for user {user.id}: {e}")
            await update.message.reply_text(BotTexts.GENERAL_ERROR)