from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    articles = relationship("ArticleDB", back_populates="category")

class ArticleDB(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=True)
    cover_image = Column(String, nullable=True)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    category = relationship("CategoryDB", back_populates="articles")
    
    # Store tags as a list of strings (PostgreSQL ARRAY)
    tags = Column(ARRAY(String), default=[])
    
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    
    view_count = Column(Integer, default=0)
    importance_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic Models

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class Category(CategoryBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    content: str
    excerpt: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: uuid.UUID
    tags: List[str] = []
    is_published: bool = False

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None

class Article(ArticleBase):
    id: uuid.UUID
    published_at: Optional[datetime] = None
    view_count: int = 0
    importance_score: float = 0.0
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ArticlePaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    pages: int

class ArticleListResponse(BaseModel):
    data: List[Article]
    meta: ArticlePaginationMeta
