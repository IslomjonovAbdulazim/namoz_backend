from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from typing import List, Optional
from datetime import datetime
import math
import uuid

from app.core.database import get_db
from app.core.auth import verify_token
from app.models.article import ArticleDB, Article, ArticleCreate, ArticleUpdate, CategoryDB, Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/admin", tags=["admin-articles"])

# --- Categories ---

@router.post("/categories", response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    # Check slug uniqueness
    existing = db.query(CategoryDB).filter(CategoryDB.slug == category_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category slug already exists")
        
    category = CategoryDB(**category_data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories", response_model=List[Category])
async def get_all_categories(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    return db.query(CategoryDB).all()

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(
    category_id: uuid.UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    update_data = category_data.dict(exclude_unset=True)
    
    # Check slug uniqueness if updating slug
    if "slug" in update_data and update_data["slug"] != category.slug:
        existing = db.query(CategoryDB).filter(CategoryDB.slug == update_data["slug"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category slug already exists")
            
    for field, value in update_data.items():
        setattr(category, field, value)
        
    db.commit()
    db.refresh(category)
    return category

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    # Check if there are related articles
    articles_count = db.query(ArticleDB).filter(ArticleDB.category_id == category_id).count()
    if articles_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete category with existing articles")
        
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}

# --- Articles ---

@router.get("/articles", response_model=dict)
async def get_all_articles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    """
    Get all articles (including unpublished) for admin table
    """
    query = db.query(ArticleDB)
    
    if category:
        query = query.join(CategoryDB).filter(CategoryDB.slug == category)
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (ArticleDB.title.ilike(search_term)) | 
            (ArticleDB.content.ilike(search_term))
        )
        
    # Default sort by created_at desc
    query = query.order_by(desc(ArticleDB.created_at))
    
    # Pagination
    total = query.count()
    offset = (page - 1) * limit
    articles = query.offset(offset).limit(limit).all()
    
    # Convert to dict format
    articles_data = []
    for article in articles:
        articles_data.append({
            "id": str(article.id),
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "cover_image": article.cover_image,
            "category_id": str(article.category_id) if article.category_id else None,
            "is_published": article.is_published,
            "published_at": article.published_at,
            "view_count": article.view_count,
            "importance_score": article.importance_score,
            "created_at": article.created_at,
            "updated_at": article.updated_at
        })
    
    return {
        "data": articles_data,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }

@router.post("/articles", response_model=Article)
async def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    # Check slug uniqueness
    existing = db.query(ArticleDB).filter(ArticleDB.slug == article_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Article slug already exists")
        
    # Check category existence
    category = db.query(CategoryDB).filter(CategoryDB.id == article_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
        
    article = ArticleDB(**article_data.dict())
    
    if article.is_published and not article.published_at:
        article.published_at = datetime.utcnow()
        
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.put("/articles/{article_id}", response_model=Article)
async def update_article(
    article_id: uuid.UUID,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    article = db.query(ArticleDB).filter(ArticleDB.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
        
    update_data = article_data.dict(exclude_unset=True)
    
    # Handle slug update uniqueness
    if "slug" in update_data and update_data["slug"] != article.slug:
        existing = db.query(ArticleDB).filter(ArticleDB.slug == update_data["slug"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Article slug already exists")
            
    for field, value in update_data.items():
        setattr(article, field, value)
        
    # Set published_at if publishing for first time
    if article.is_published and not article.published_at:
        article.published_at = datetime.utcnow()
        
    db.commit()
    db.refresh(article)
    return article

@router.delete("/articles/{article_id}")
async def delete_article(
    article_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    article = db.query(ArticleDB).filter(ArticleDB.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
        
    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}

# --- Importance Calculation ---

@router.post("/articles/calculate-importance")
async def calculate_importance(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    """
    Recalculate importance score for all articles.
    Logic: score = log(view_count + 1) * 10 + (100 / days_since_published + 1)
    """
    articles = db.query(ArticleDB).filter(ArticleDB.is_published == True).all()
    now = datetime.utcnow()
    count = 0
    
    for article in articles:
        days_since = 1
        if article.published_at:
            delta = now - article.published_at
            days_since = max(1, delta.days)
            
        # Logarithmic view count impact (diminishing returns)
        view_score = math.log10(article.view_count + 1) * 10
        
        # Freshness impact (decays over time)
        freshness_score = 100 / days_since
        
        article.importance_score = view_score + freshness_score
        count += 1
        
    db.commit()
    return {"message": f"Recalculated importance for {count} articles"}

# --- Stats ---

@router.get("/articles/stats")
async def get_article_stats(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    total_views = db.query(func.sum(ArticleDB.view_count)).scalar() or 0
    total_articles = db.query(func.count(ArticleDB.id)).scalar() or 0
    published_articles = db.query(func.count(ArticleDB.id)).filter(ArticleDB.is_published == True).scalar() or 0
    
    current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_this_month = db.query(func.count(ArticleDB.id)).filter(
        ArticleDB.published_at >= current_month
    ).scalar() or 0
    
    most_read = db.query(ArticleDB).order_by(desc(ArticleDB.view_count)).first()
    
    return {
        "total_views": total_views,
        "total_articles": total_articles,
        "published_articles": published_articles,
        "new_this_month": new_this_month,
        "most_read_article": {
            "title": most_read.title,
            "views": most_read.view_count
        } if most_read else None
    }

# --- File Upload ---

@router.post("/articles/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    MAX_FILE_SIZE = 500 * 1024  # 500KB
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
    
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, or WEBP images are allowed")
        
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 500KB)")
        
    from app.services.storage import storage_service
    
    try:
        url = storage_service.upload_file(file, "images")
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
