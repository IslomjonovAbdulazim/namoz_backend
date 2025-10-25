#!/usr/bin/env python3
import asyncio
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.config import bot_config
from bot.services.api_client import APIClient
from bot.services.user_service import UserService
from bot.handlers.commands import CommandHandler as BotCommandHandler
from bot.handlers.callbacks import CallbackHandler
from bot.handlers.registration import RegistrationHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, bot_config.LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

class StudentBot:
    def __init__(self):
        self.application = None
        self.api_client = None
        self.user_service = None
        self.command_handler = None
        self.callback_handler = None
        self.registration_handler = None
    
    async def initialize(self):
        """Initialize bot components"""
        logger.info("Initializing Student Bot...")
        
        # Initialize API client
        self.api_client = APIClient(bot_config.API_BASE_URL)
        await self.api_client.initialize()
        
        # Initialize services
        self.user_service = UserService(self.api_client)
        
        # Initialize handlers
        self.command_handler = BotCommandHandler(self.user_service)
        self.callback_handler = CallbackHandler(self.user_service)
        self.registration_handler = RegistrationHandler(self.user_service)
        
        # Initialize Telegram application with proper timeouts
        self.application = (
            Application.builder()
            .token(bot_config.BOT_TOKEN)
            .connection_pool_size(10)
            .pool_timeout(bot_config.POOL_TIMEOUT)
            .read_timeout(bot_config.READ_TIMEOUT)
            .write_timeout(bot_config.WRITE_TIMEOUT)
            .connect_timeout(bot_config.CONNECT_TIMEOUT)
            .build()
        )
        
        # Add error handler
        self.application.add_error_handler(self.error_handler)
        
        # Add command handlers
        self.application.add_handler(
            CommandHandler("start", self.command_handler.start_command)
        )
        self.application.add_handler(
            CommandHandler("lessons", self.command_handler.lessons_command)
        )
        self.application.add_handler(
            CommandHandler("results", self.command_handler.results_command)
        )
        self.application.add_handler(
            CommandHandler("help", self.command_handler.help_command)
        )
        self.application.add_handler(
            CommandHandler("profile", self.command_handler.profile_command)
        )
        
        # Add callback handler
        self.application.add_handler(
            CallbackQueryHandler(self.callback_handler.handle_callback)
        )
        
        # Add contact handler for phone number sharing
        self.application.add_handler(
            MessageHandler(filters.CONTACT, self.registration_handler.handle_contact)
        )
        
        logger.info("Bot initialization completed")
    
    async def error_handler(self, update, context):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        # Try to send error message to user
        try:
            if update and update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ Xatolik yuz berdi. Qaytadan urinib ko'ring yoki administrator bilan bog'laning."
                )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up bot resources...")
        if self.api_client:
            await self.api_client.close()
    
    async def run(self):
        """Run the bot"""
        try:
            await self.initialize()
            
            # Test bot token validity first
            logger.info("Testing bot token...")
            await self.application.initialize()
            bot_info = await self.application.bot.get_me()
            logger.info(f"Bot connected successfully: @{bot_info.username}")
            
            await self.application.start()
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"]
            )
            
            logger.info("Bot started successfully. Press Ctrl+C to stop.")
            
            # Keep the bot running
            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                logger.info("Received interrupt signal. Stopping bot...")
                
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            if "Unauthorized" in str(e):
                logger.error("Bot token is invalid or revoked. Please check your BOT_TOKEN in .env file.")
            elif "TimedOut" in str(e) or "ConnectTimeout" in str(e):
                logger.error("Connection timeout. Check your internet connection or try again later.")
            raise
        finally:
            try:
                if hasattr(self, 'application') and self.application:
                    await self.application.stop()
            except Exception as cleanup_error:
                logger.error(f"Error during cleanup: {cleanup_error}")
            await self.cleanup()

async def main():
    """Main entry point"""
    bot = StudentBot()
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())