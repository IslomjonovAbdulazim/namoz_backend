import logging
from typing import Optional, Dict, Any
from bot.services.api_client import APIClient
from bot.utils.helpers import get_user_display_name, format_phone_number

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, api_client: APIClient):
        self.api = api_client
    
    async def is_user_registered(self, telegram_id: int) -> bool:
        """Check if user is registered in the system"""
        return await self.api.check_user_exists(telegram_id)
    
    async def register_user(self, telegram_user, phone_number: str) -> bool:
        """Register new user with phone number"""
        try:
            full_name = get_user_display_name(telegram_user)
            formatted_phone = format_phone_number(phone_number)
            
            logger.info(f"Registering user: {telegram_user.id} - {full_name} - {formatted_phone}")
            
            success = await self.api.register_user(
                telegram_id=telegram_user.id,
                full_name=full_name,
                phone_number=formatted_phone
            )
            
            if success:
                logger.info(f"User registered successfully: {telegram_user.id}")
            else:
                logger.error(f"Failed to register user: {telegram_user.id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error registering user {telegram_user.id}: {e}")
            return False
    
    async def get_user_lessons(self, telegram_id: int) -> Optional[list]:
        """Get lessons for registered user"""
        return await self.api.get_user_lessons(telegram_id)
    
    async def get_lesson_detail(self, telegram_id: int, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Get lesson details for user"""
        return await self.api.get_lesson_detail(telegram_id, lesson_id)
    
    async def get_user_results(self, telegram_id: int) -> Optional[list]:
        """Get test results for user"""
        return await self.api.get_user_results(telegram_id)