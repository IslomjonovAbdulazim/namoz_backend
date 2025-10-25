#!/usr/bin/env python3
"""
Simple script to test bot token validity
"""
import asyncio
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

async def test_bot_token():
    """Test if bot token is valid"""
    bot_token = os.getenv("BOT_TOKEN")
    
    if not bot_token:
        print("❌ BOT_TOKEN not found in .env file")
        return False
    
    print(f"🔄 Testing bot token: {bot_token[:10]}...")
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{bot_token}/getMe"
            
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("ok"):
                        bot_info = data.get("result", {})
                        print(f"✅ Bot token is valid!")
                        print(f"   Bot name: {bot_info.get('first_name')}")
                        print(f"   Username: @{bot_info.get('username')}")
                        print(f"   Bot ID: {bot_info.get('id')}")
                        return True
                    else:
                        print(f"❌ Bot API returned error: {data.get('description')}")
                        return False
                elif response.status == 401:
                    print("❌ Bot token is invalid or unauthorized")
                    return False
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    return False
                    
    except asyncio.TimeoutError:
        print("❌ Connection timeout - check your internet connection")
        return False
    except Exception as e:
        print(f"❌ Error testing bot token: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_bot_token())