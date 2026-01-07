from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from typing import List, Optional
import uuid

from app.core.database import get_db
from app.models.article import ArticleDB, Article, CategoryDB, Category

router = APIRouter(prefix="/v1/articles", tags=["articles"])

@router.get("", response_model=dict)
async def get_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = Query("latest", regex="^(latest|popular|important)$"),
    db: Session = Depends(get_db)
):
    query = db.query(ArticleDB).filter(ArticleDB.is_published == True)
    
    # Filter by category slug
    if category:
        query = query.join(CategoryDB).filter(CategoryDB.slug == category)
        
    # Filter by tag
    if tag:
        # PostgreSQL array overlap check
        # This assumes tags are stored as ARRAY(String)
        query = query.filter(ArticleDB.tags.contains([tag]))
        
    # Search in title or content
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (ArticleDB.title.ilike(search_term)) | 
            (ArticleDB.content.ilike(search_term))
        )
        
    # Sorting
    if sort == "latest":
        query = query.order_by(desc(ArticleDB.published_at))
    elif sort == "popular":
        query = query.order_by(desc(ArticleDB.view_count))
    elif sort == "important":
        query = query.order_by(desc(ArticleDB.importance_score))
        
    # Pagination
    total = query.count()
    offset = (page - 1) * limit
    articles = query.offset(offset).limit(limit).all()
    
    return {
        "data": articles,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }

@router.get("/categories", response_model=List[Category])
async def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryDB).all()

@router.get("/{slug}", response_model=Article)
async def get_article(
    slug: str,
    db: Session = Depends(get_db)
):
    article = db.query(ArticleDB).filter(
        ArticleDB.slug == slug,
        ArticleDB.is_published == True
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
        
    # Increment view count
    article.view_count += 1
    db.commit()
    db.refresh(article)
    
    return article
