from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class UserLessonAccessDB(Base):
    __tablename__ = "user_lesson_access"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), index=True)
    is_unlocked = Column(Boolean, default=True, index=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow, index=True)
    amount = Column(Integer, nullable=False)
    paid_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    user = relationship("UserDB")
    lesson = relationship("LessonDB")


class UserLessonAccess(BaseModel):
    id: str = Field(..., index=True)
    user_id: str = Field(..., index=True)
    lesson_id: str = Field(..., index=True)
    is_unlocked: bool = Field(default=True, index=True)
    unlocked_at: Optional[datetime] = Field(default=None, index=True)
    amount: int = Field(..., ge=0)
    paid_at: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }