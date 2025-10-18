from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class UserTestResultDB(Base):
    __tablename__ = "user_test_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), index=True)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, index=True)
    ended_at = Column(DateTime, nullable=False)
    
    user = relationship("UserDB")
    lesson = relationship("LessonDB")


class UserAnswer(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    user_selected: str = Field(..., min_length=1, max_length=500)
    correct: str = Field(..., min_length=1, max_length=500)


class UserTestResult(BaseModel):
    id: str = Field(..., index=True)
    user_id: str = Field(..., index=True)
    lesson_id: str = Field(..., index=True)
    score: int = Field(..., ge=0)
    total_questions: int = Field(..., ge=1)
    answers: List[UserAnswer] = Field(..., min_items=1)
    started_at: datetime = Field(..., index=True)
    ended_at: datetime

    @validator('score')
    def validate_score(cls, v, values):
        if 'total_questions' in values and v > values['total_questions']:
            raise ValueError('score cannot exceed total_questions')
        return v

    @validator('ended_at')
    def validate_ended_at(cls, v, values):
        if 'started_at' in values and v < values['started_at']:
            raise ValueError('ended_at must be after started_at')
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }