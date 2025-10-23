import aiohttp
import logging
from typing import Dict, List, Optional, Any
from bot.utils.helpers import log_user_action

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request to API"""
        if not self.session:
            await self.initialize()
        
        try:
            url = f"{self.base_url}{endpoint}"
            async with self.session.request(method, url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    logger.warning(f"API endpoint not found: {endpoint}")
                    return None
                else:
                    error_text = await response.text()
                    logger.error(f"API request failed: {response.status} - {error_text}")
                    return None
        except Exception as e:
            logger.error(f"API request error for {endpoint}: {e}")
            return None
    
    async def get_user_lessons(self, telegram_id: int) -> Optional[List[Dict[str, Any]]]:
        """Get lessons for user"""
        log_user_action(telegram_id, "get_lessons")
        return await self._request("GET", f"/bot/user/{telegram_id}/lessons")
    
    async def get_lesson_detail(self, telegram_id: int, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Get lesson details"""
        log_user_action(telegram_id, "get_lesson_detail", lesson_id)
        return await self._request("GET", f"/bot/user/{telegram_id}/lesson/{lesson_id}")
    
    async def get_lesson_questions(self, telegram_id: int, lesson_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get test questions for lesson"""
        log_user_action(telegram_id, "get_questions", lesson_id)
        return await self._request("GET", f"/bot/user/{telegram_id}/lesson/{lesson_id}/questions")
    
    async def submit_test(self, telegram_id: int, lesson_id: str, answers: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Submit test answers"""
        log_user_action(telegram_id, "submit_test", f"{lesson_id} - {len(answers)} answers")
        return await self._request("POST", f"/bot/user/{telegram_id}/lesson/{lesson_id}/test", {"answers": answers})
    
    async def get_user_results(self, telegram_id: int) -> Optional[List[Dict[str, Any]]]:
        """Get user test results"""
        log_user_action(telegram_id, "get_results")
        return await self._request("GET", f"/bot/user/{telegram_id}/results")
    
    async def get_result_detail(self, telegram_id: int, result_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed test result"""
        log_user_action(telegram_id, "get_result_detail", result_id)
        return await self._request("GET", f"/bot/user/{telegram_id}/result/{result_id}")
    
    async def check_user_exists(self, telegram_id: int) -> bool:
        """Check if user exists in the system"""
        log_user_action(telegram_id, "check_user_exists")
        
        # Try to get user lessons - if successful, user exists
        result = await self.get_user_lessons(telegram_id)
        return result is not None
    
    async def register_user(self, telegram_id: int, full_name: str, phone_number: str) -> bool:
        """Register new user"""
        log_user_action(telegram_id, "register_user", f"{full_name} - {phone_number}")
        
        # This endpoint might not exist yet, we'll need to create it
        # For now, we'll assume registration happens automatically when user makes first API call
        # or we can create a separate registration endpoint
        
        user_data = {
            "full_name": full_name,
            "telegram_id": telegram_id,
            "phone_number": phone_number
        }
        
        result = await self._request("POST", "/bot/register", user_data)
        return result is not None