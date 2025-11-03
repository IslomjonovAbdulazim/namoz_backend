from datetime import datetime
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re
from app.core.database import Base


class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    full_name = Column(String(100), nullable=False)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    phone_number = Column(String(20), index=True, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, index=True)


class User(BaseModel):
    id: str = Field(..., index=True)
    full_name: str = Field(..., min_length=1, max_length=100)
    telegram_id: int = Field(..., index=True, unique=True)
    phone_number: str = Field(..., index=True)
    joined_at: datetime = Field(..., index=True)

    @validator('phone_number')
    def validate_phone_number(cls, v):
        pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number format')
        return v

    @validator('telegram_id')
    def validate_telegram_id(cls, v):
        if v <= 0:
            raise ValueError('telegram_id must be positive')
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }