from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class LessonDB(Base):
    __tablename__ = "lessons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    video_url = Column(String(500), nullable=False)
    pdf_url = Column(String(500), nullable=False)
    ppt_url = Column(String(500), nullable=False)
    is_published = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    questions = relationship("TestQuestionDB", back_populates="lesson")


class Lesson(BaseModel):
    id: str = Field(..., index=True)
    title: str = Field(..., min_length=1, max_length=200, index=True)
    description: str = Field(..., min_length=1, max_length=2000)
    video_url: HttpUrl
    pdf_url: HttpUrl
    ppt_url: HttpUrl
    is_published: bool = Field(default=True, index=True)
    created_at: datetime = Field(..., index=True)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }