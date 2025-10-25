import os
from dotenv import load_dotenv

load_dotenv()

class BotConfig:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Connection settings
    CONNECTION_TIMEOUT: int = int(os.getenv("CONNECTION_TIMEOUT", "30"))
    READ_TIMEOUT: int = int(os.getenv("READ_TIMEOUT", "30"))
    WRITE_TIMEOUT: int = int(os.getenv("WRITE_TIMEOUT", "30"))
    CONNECT_TIMEOUT: int = int(os.getenv("CONNECT_TIMEOUT", "30"))
    POOL_TIMEOUT: int = int(os.getenv("POOL_TIMEOUT", "30"))
    
    def __post_init__(self):
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")

bot_config = BotConfig()