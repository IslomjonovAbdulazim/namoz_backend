from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import verify_admin_credentials, create_access_token, verify_token
from app.models import *
from app.services.storage import storage_service
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

class AdminLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

@router.post("/auth/login", response_model=TokenResponse)
async def admin_login(credentials: AdminLogin):
    if not verify_admin_credentials(credentials.email, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )
    
    access_token = create_access_token(data={"sub": credentials.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600
    }

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    users = db.query(UserDB).all()
    result = []
    
    for user in users:
        total_spent = db.query(func.sum(UserLessonAccessDB.amount)).filter(
            UserLessonAccessDB.user_id == user.id
        ).scalar() or 0
        
        total_lessons = db.query(func.count(UserLessonAccessDB.id)).filter(
            UserLessonAccessDB.user_id == user.id
        ).scalar() or 0
        
        result.append({
            "id": str(user.id),
            "full_name": user.full_name,
            "telegram_id": user.telegram_id,
            "phone_number": user.phone_number,
            "joined_at": user.joined_at,
            "total_lessons_purchased": total_lessons,
            "total_spent": total_spent
        })
    
    return result


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete related records first
    db.query(UserLessonAccessDB).filter(UserLessonAccessDB.user_id == user_id).delete()
    db.query(UserTestResultDB).filter(UserTestResultDB.user_id == user_id).delete()
    
    # Delete user
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

class LessonCreate(BaseModel):
    title: str
    description: str
    video_url: str

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    pdf_url: Optional[str] = None
    ppt_url: Optional[str] = None

class LessonPublish(BaseModel):
    is_published: bool

@router.get("/lessons")
async def get_all_lessons(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lessons = db.query(LessonDB).all()
    result = []
    
    for lesson in lessons:
        total_users = db.query(func.count(UserLessonAccessDB.id)).filter(
            UserLessonAccessDB.lesson_id == lesson.id
        ).scalar() or 0
        
        total_revenue = db.query(func.sum(UserLessonAccessDB.amount)).filter(
            UserLessonAccessDB.lesson_id == lesson.id
        ).scalar() or 0
        
        avg_score = db.query(func.avg(UserTestResultDB.score)).filter(
            UserTestResultDB.lesson_id == lesson.id
        ).scalar() or 0
        
        result.append({
            "id": str(lesson.id),
            "title": lesson.title,
            "description": lesson.description,
            "video_url": lesson.video_url,
            "pdf_url": lesson.pdf_url,
            "ppt_url": lesson.ppt_url,
            "is_published": lesson.is_published,
            "created_at": lesson.created_at,
            "total_users": total_users,
            "total_revenue": total_revenue,
            "average_score": round(float(avg_score), 1) if avg_score else 0
        })
    
    return result

@router.post("/lessons")
async def create_lesson(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = LessonDB(
        title=lesson_data.title,
        description=lesson_data.description,
        video_url=lesson_data.video_url,
        pdf_url="",  # Will be uploaded separately
        ppt_url="",  # Will be uploaded separately
        is_published=False  # Always false when creating
    )
    
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    
    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "description": lesson.description,
        "video_url": lesson.video_url,
        "pdf_url": lesson.pdf_url,
        "ppt_url": lesson.ppt_url,
        "is_published": lesson.is_published,
        "created_at": lesson.created_at
    }

@router.put("/lessons/{lesson_id}")
async def update_lesson(
    lesson_id: str,
    lesson_data: LessonUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    update_data = lesson_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)
    
    db.commit()
    db.refresh(lesson)
    
    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "description": lesson.description,
        "video_url": lesson.video_url,
        "pdf_url": lesson.pdf_url,
        "ppt_url": lesson.ppt_url,
        "is_published": lesson.is_published,
        "created_at": lesson.created_at
    }

@router.delete("/lessons/{lesson_id}")
async def delete_lesson(
    lesson_id: str,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Delete related records
    db.query(TestQuestionDB).filter(TestQuestionDB.lesson_id == lesson_id).delete()
    db.query(UserLessonAccessDB).filter(UserLessonAccessDB.lesson_id == lesson_id).delete()
    db.query(UserTestResultDB).filter(UserTestResultDB.lesson_id == lesson_id).delete()
    
    db.delete(lesson)
    db.commit()
    
    return {"message": "Lesson deleted successfully"}

@router.put("/lessons/{lesson_id}/publish")
async def publish_lesson(
    lesson_id: str,
    publish_data: LessonPublish,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson.is_published = publish_data.is_published
    db.commit()
    
    return {
        "id": str(lesson.id),
        "title": lesson.title,
        "is_published": lesson.is_published,
        "updated_at": datetime.utcnow()
    }

# File Upload Endpoints
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@router.post("/lessons/{lesson_id}/upload/pdf")
async def upload_lesson_pdf(
    lesson_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    # Check if lesson exists
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Validate file
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")
    
    # Upload file
    pdf_url = storage_service.upload_file(file, "pdfs")
    
    # Update lesson
    lesson.pdf_url = pdf_url
    db.commit()
    
    return {"pdf_url": pdf_url, "lesson_id": lesson_id}

@router.post("/lessons/{lesson_id}/upload/ppt")
async def upload_lesson_ppt(
    lesson_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    # Check if lesson exists
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Validate file
    allowed_types = [
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PPT/PPTX files are allowed")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")
    
    # Upload file
    ppt_url = storage_service.upload_file(file, "presentations")
    
    # Update lesson
    lesson.ppt_url = ppt_url
    db.commit()
    
    return {"ppt_url": ppt_url, "lesson_id": lesson_id}

# Question Management Endpoints
class QuestionCreate(BaseModel):
    question_text: str
    options: List[str]
    correct_option: int

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option: Optional[int] = None

@router.get("/lessons/{lesson_id}/questions")
async def get_lesson_questions(
    lesson_id: str,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    questions = db.query(TestQuestionDB).filter(
        TestQuestionDB.lesson_id == lesson_id
    ).all()
    
    return [
        {
            "id": str(question.id),
            "lesson_id": str(question.lesson_id),
            "question_text": question.question_text,
            "options": question.options,
            "correct_option": question.correct_option
        }
        for question in questions
    ]

@router.post("/lessons/{lesson_id}/questions")
async def create_question(
    lesson_id: str,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    if question_data.correct_option >= len(question_data.options):
        raise HTTPException(
            status_code=400, 
            detail="correct_option must be within options range"
        )
    
    question = TestQuestionDB(
        lesson_id=lesson_id,
        question_text=question_data.question_text,
        options=question_data.options,
        correct_option=question_data.correct_option
    )
    
    db.add(question)
    db.commit()
    db.refresh(question)
    
    return {
        "id": str(question.id),
        "lesson_id": str(question.lesson_id),
        "question_text": question.question_text,
        "options": question.options,
        "correct_option": question.correct_option
    }

@router.put("/questions/{question_id}")
async def update_question(
    question_id: str,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    question = db.query(TestQuestionDB).filter(
        TestQuestionDB.id == question_id
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_data = question_data.dict(exclude_unset=True)
    
    # Validate correct_option if provided
    if "correct_option" in update_data:
        options = update_data.get("options", question.options)
        if update_data["correct_option"] >= len(options):
            raise HTTPException(
                status_code=400,
                detail="correct_option must be within options range"
            )
    
    for field, value in update_data.items():
        setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    
    return {
        "id": str(question.id),
        "lesson_id": str(question.lesson_id),
        "question_text": question.question_text,
        "options": question.options,
        "correct_option": question.correct_option
    }

@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: str,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    question = db.query(TestQuestionDB).filter(
        TestQuestionDB.id == question_id
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(question)
    db.commit()
    
    return {"message": "Question deleted successfully"}

# Analytics & Reports Endpoints
@router.get("/lessons/{lesson_id}/analytics")
async def get_lesson_analytics(
    lesson_id: str,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Basic stats
    total_students = db.query(func.count(UserLessonAccessDB.id)).filter(
        UserLessonAccessDB.lesson_id == lesson_id
    ).scalar() or 0
    
    total_revenue = db.query(func.sum(UserLessonAccessDB.amount)).filter(
        UserLessonAccessDB.lesson_id == lesson_id
    ).scalar() or 0
    
    avg_score = db.query(func.avg(UserTestResultDB.score)).filter(
        UserTestResultDB.lesson_id == lesson_id
    ).scalar() or 0
    
    # Completion rate
    test_takers = db.query(func.count(UserTestResultDB.id.distinct())).filter(
        UserTestResultDB.lesson_id == lesson_id
    ).scalar() or 0
    
    completion_rate = (test_takers / total_students * 100) if total_students > 0 else 0
    
    # Recent purchases
    recent_purchases = db.query(
        UserLessonAccessDB, UserDB
    ).join(UserDB).filter(
        UserLessonAccessDB.lesson_id == lesson_id
    ).order_by(desc(UserLessonAccessDB.paid_at)).limit(10).all()
    
    return {
        "lesson_id": str(lesson.id),
        "lesson_title": lesson.title,
        "total_students": total_students,
        "total_revenue": total_revenue,
        "average_score": round(float(avg_score), 1) if avg_score else 0,
        "completion_rate": round(completion_rate, 1),
        "recent_purchases": [
            {
                "user_id": str(user.id),
                "user_name": user.full_name,
                "amount": access.amount,
                "paid_at": access.paid_at
            }
            for access, user in recent_purchases
        ]
    }

@router.get("/lessons/{lesson_id}/results")
async def get_lesson_results(
    lesson_id: str,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    results = db.query(
        UserTestResultDB, UserDB
    ).join(UserDB).filter(
        UserTestResultDB.lesson_id == lesson_id
    ).order_by(desc(UserTestResultDB.ended_at)).all()
    
    result_list = []
    for result, user in results:
        # Calculate completion time
        time_diff = result.ended_at - result.started_at
        hours, remainder = divmod(time_diff.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        completion_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        result_list.append({
            "id": str(result.id),
            "user_id": str(user.id),
            "user_name": user.full_name,
            "score": result.score,
            "total_questions": result.total_questions,
            "completion_time": completion_time,
            "started_at": result.started_at,
            "ended_at": result.ended_at
        })
    
    return result_list

@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    # Basic totals
    total_users = db.query(func.count(UserDB.id)).scalar() or 0
    total_lessons = db.query(func.count(LessonDB.id)).scalar() or 0
    total_revenue = db.query(func.sum(UserLessonAccessDB.amount)).scalar() or 0
    
    # Monthly stats
    current_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_revenue = db.query(func.sum(UserLessonAccessDB.amount)).filter(
        UserLessonAccessDB.paid_at >= current_month
    ).scalar() or 0
    
    new_users_this_month = db.query(func.count(UserDB.id)).filter(
        UserDB.joined_at >= current_month
    ).scalar() or 0
    
    # Most popular lessons
    popular_lessons = db.query(
        LessonDB,
        func.count(UserLessonAccessDB.id).label('student_count'),
        func.sum(UserLessonAccessDB.amount).label('revenue')
    ).join(UserLessonAccessDB).group_by(LessonDB.id).order_by(
        desc('student_count')
    ).limit(5).all()
    
    # Recent activity (last 20 activities)
    recent_purchases = db.query(
        UserLessonAccessDB, UserDB, LessonDB
    ).join(UserDB).join(LessonDB).order_by(
        desc(UserLessonAccessDB.paid_at)
    ).limit(10).all()
    
    recent_tests = db.query(
        UserTestResultDB, UserDB, LessonDB
    ).join(UserDB).join(LessonDB).order_by(
        desc(UserTestResultDB.ended_at)
    ).limit(10).all()
    
    # Combine and sort activities
    activities = []
    
    for access, user, lesson in recent_purchases:
        activities.append({
            "type": "purchase",
            "user_name": user.full_name,
            "lesson_title": lesson.title,
            "amount": access.amount,
            "timestamp": access.paid_at
        })
    
    for result, user, lesson in recent_tests:
        activities.append({
            "type": "test_completion",
            "user_name": user.full_name,
            "lesson_title": lesson.title,
            "score": result.score,
            "timestamp": result.ended_at
        })
    
    # Sort by timestamp and limit
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    activities = activities[:20]
    
    return {
        "total_users": total_users,
        "total_lessons": total_lessons,
        "total_revenue": total_revenue,
        "monthly_revenue": monthly_revenue,
        "new_users_this_month": new_users_this_month,
        "most_popular_lessons": [
            {
                "lesson_id": str(lesson.id),
                "title": lesson.title,
                "student_count": student_count,
                "revenue": revenue or 0
            }
            for lesson, student_count, revenue in popular_lessons
        ],
        "recent_activity": activities
    }

# Access Management Endpoints
@router.get("/access/all")
async def get_all_access(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    access_records = db.query(
        UserLessonAccessDB, UserDB, LessonDB
    ).join(UserDB).join(LessonDB).order_by(
        desc(UserLessonAccessDB.paid_at)
    ).all()
    
    return [
        {
            "id": str(access.id),
            "user_id": str(user.id),
            "user_name": user.full_name,
            "lesson_id": str(lesson.id),
            "lesson_title": lesson.title,
            "amount": access.amount,
            "paid_at": access.paid_at,
            "notes": access.notes
        }
        for access, user, lesson in access_records
    ]

class GrantAccessRequest(BaseModel):
    user_id: str
    lesson_id: str
    amount: int = 0
    notes: str = "Admin granted access"

@router.post("/access/grant")
async def grant_access(
    request: GrantAccessRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(verify_token)
):
    # Check if user exists
    user = db.query(UserDB).filter(UserDB.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if lesson exists
    lesson = db.query(LessonDB).filter(LessonDB.id == request.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Check if access already exists
    existing_access = db.query(UserLessonAccessDB).filter(
        UserLessonAccessDB.user_id == request.user_id,
        UserLessonAccessDB.lesson_id == request.lesson_id
    ).first()
    
    if existing_access:
        raise HTTPException(status_code=400, detail="User already has access to this lesson")
    
    # Create access record
    access = UserLessonAccessDB(
        user_id=request.user_id,
        lesson_id=request.lesson_id,
        amount=request.amount,
        notes=request.notes,
        is_unlocked=True,
        unlocked_at=datetime.utcnow(),
        paid_at=datetime.utcnow()
    )
    
    db.add(access)
    db.commit()
    db.refresh(access)
    
    return {
        "id": str(access.id),
        "user_id": str(access.user_id),
        "lesson_id": str(access.lesson_id),
        "is_unlocked": access.is_unlocked,
        "unlocked_at": access.unlocked_at,
        "amount": access.amount,
        "paid_at": access.paid_at,
        "notes": access.notes
    }