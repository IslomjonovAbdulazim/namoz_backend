from typing import List
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, Text, Integer, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class TestQuestionDB(Base):
    __tablename__ = "test_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), index=True)
    question_text = Column(Text, nullable=False)
    options = Column(ARRAY(String), nullable=False)
    correct_option = Column(Integer, nullable=False)
    
    lesson = relationship("LessonDB", back_populates="questions")


class TestQuestion(BaseModel):
    id: str = Field(..., index=True)
    lesson_id: str = Field(..., index=True)
    question_text: str = Field(..., min_length=1, max_length=1000)
    options: List[str] = Field(..., min_items=2, max_items=10)
    correct_option: int = Field(..., ge=0)

    @validator('correct_option')
    def validate_correct_option(cls, v, values):
        if 'options' in values and v >= len(values['options']):
            raise ValueError('correct_option must be within options range')
        return v

    @validator('options')
    def validate_options(cls, v):
        if len(set(v)) != len(v):
            raise ValueError('options must be unique')
        for option in v:
            if not option.strip():
                raise ValueError('options cannot be empty')
        return v