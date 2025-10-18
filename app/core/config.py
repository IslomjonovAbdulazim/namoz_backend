import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "fallback-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_HOURS: int = int(os.getenv("JWT_EXPIRE_HOURS", "24"))
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_BUCKET: str = os.getenv("GOOGLE_CLOUD_BUCKET")
    GOOGLE_CLOUD_PRIVATE_KEY: str = os.getenv("GOOGLE_CLOUD_PRIVATE_KEY")
    GOOGLE_CLOUD_CLIENT_EMAIL: str = os.getenv("GOOGLE_CLOUD_CLIENT_EMAIL")
    GOOGLE_CLOUD_PRIVATE_KEY_ID: str = os.getenv("GOOGLE_CLOUD_PRIVATE_KEY_ID")
    GOOGLE_CLOUD_CLIENT_ID: str = os.getenv("GOOGLE_CLOUD_CLIENT_ID")

settings = Settings()