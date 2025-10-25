from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import UserDB
from app.models.lesson import LessonDB
from app.models.test_result import UserTestResultDB
from app.models.test_question import TestQuestionDB
from app.models.access import UserLessonAccessDB
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bot", tags=["Bot API"])

# Pydantic models
class UserRegistration(BaseModel):
    telegram_id: int
    full_name: str
    phone_number: str

class TestAnswer(BaseModel):
    question_id: int
    selected_option: int

class TestSubmission(BaseModel):
    answers: List[TestAnswer]

# Bot API endpoints
@router.post("/register")
async def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    """Register a new user from Telegram bot"""
    try:
        # Check if user already exists
        existing_user = db.query(UserDB).filter(UserDB.telegram_id == user_data.telegram_id).first()
        if existing_user:
            return {"message": "User already registered", "user_id": str(existing_user.id)}
        
        # Create new user
        new_user = UserDB(
            telegram_id=user_data.telegram_id,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"User registered: {user_data.telegram_id} - {user_data.full_name}")
        
        return {
            "message": "User registered successfully",
            "user_id": str(new_user.id),
            "telegram_id": new_user.telegram_id
        }
        
    except Exception as e:
        logger.error(f"Error registering user {user_data.telegram_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Registration failed")

@router.get("/user/{telegram_id}/lessons")
async def get_user_lessons(telegram_id: int, db: Session = Depends(get_db)):
    """Get lessons available to user"""
    try:
        # Get user
        user = db.query(UserDB).filter(UserDB.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get all lessons with access information
        lessons = db.query(LessonDB).all()
        result = []
        
        for lesson in lessons:
            # Check if user has access
            access = db.query(UserLessonAccessDB).filter(
                UserLessonAccessDB.user_id == user.id,
                UserLessonAccessDB.lesson_id == lesson.id
            ).first()
            
            has_access = access is not None
            
            # Get test result if user has taken the test
            test_result = None
            score = None
            if has_access:
                test_result = db.query(UserTestResultDB).filter(
                    UserTestResultDB.user_id == user.id,
                    UserTestResultDB.lesson_id == lesson.id
                ).first()
                if test_result:
                    score = test_result.score
            
            lesson_data = {
                "id": str(lesson.id),
                "title": lesson.title,
                "description": lesson.description,
                "price": access.amount if access else 0,  # Price from access record
                "has_access": has_access,
                "score": score,
                "test_completed": test_result is not None
            }
            result.append(lesson_data)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting lessons for user {telegram_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get lessons")

@router.get("/user/{telegram_id}/lesson/{lesson_id}")
async def get_lesson_detail(telegram_id: int, lesson_id: int, db: Session = Depends(get_db)):
    """Get detailed lesson information"""
    try:
        # Get user
        user = db.query(UserDB).filter(UserDB.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get lesson
        lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        # Check access
        access = db.query(UserLessonAccessDB).filter(
            UserLessonAccessDB.user_id == user.id,
            UserLessonAccessDB.lesson_id == lesson.id
        ).first()
        
        has_access = access is not None
        
        # Get test result
        test_result = db.query(UserTestResultDB).filter(
            UserTestResultDB.user_id == user.id,
            UserTestResultDB.lesson_id == lesson.id
        ).first()
        
        lesson_data = {
            "id": str(lesson.id),
            "title": lesson.title,
            "description": lesson.description,
            "content": lesson.description if has_access else None,  # No content field in model
            "video_url": lesson.video_url if has_access else None,
            "pdf_url": lesson.pdf_url if has_access else None,
            "presentation_url": lesson.ppt_url if has_access else None,  # ppt_url not presentation_url
            "price": access.amount if access else 0,
            "has_access": has_access,
            "test_completed": test_result is not None,
            "score": test_result.score if test_result else None
        }
        
        return lesson_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting lesson detail for user {telegram_id}, lesson {lesson_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get lesson detail")

@router.get("/user/{telegram_id}/lesson/{lesson_id}/questions")
async def get_lesson_questions(telegram_id: int, lesson_id: int, db: Session = Depends(get_db)):
    """Get test questions for lesson"""
    try:
        # Get user
        user = db.query(UserDB).filter(UserDB.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check access
        access = db.query(UserLessonAccessDB).filter(
            UserLessonAccessDB.user_id == user.id,
            UserLessonAccessDB.lesson_id == lesson_id
        ).first()
        
        if not access:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get questions
        questions = db.query(TestQuestionDB).filter(TestQuestionDB.lesson_id == lesson_id).all()
        
        result = []
        for question in questions:
            question_data = {
                "id": str(question.id),
                "question_text": question.question_text,
                "options": question.options  # options is an array field
            }
            result.append(question_data)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting questions for user {telegram_id}, lesson {lesson_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get questions")

@router.post("/user/{telegram_id}/lesson/{lesson_id}/test")
async def submit_test(telegram_id: int, lesson_id: int, submission: TestSubmission, db: Session = Depends(get_db)):
    """Submit test answers"""
    try:
        # Get user
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check access
        access = db.query(Access).filter(
            Access.user_id == user.id,
            Access.lesson_id == lesson_id
        ).first()
        
        if not access:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get questions
        questions = db.query(TestQuestion).filter(TestQuestion.lesson_id == lesson_id).all()
        question_dict = {q.id: q for q in questions}
        
        # Calculate score
        correct_answers = 0
        total_questions = len(questions)
        
        for answer in submission.answers:
            question = question_dict.get(answer.question_id)
            if question and question.correct_option == answer.selected_option:
                correct_answers += 1
        
        score = round((correct_answers / total_questions) * 100) if total_questions > 0 else 0
        passed = score >= 70  # 70% passing score
        
        # Delete existing result if any
        existing_result = db.query(TestResult).filter(
            TestResult.user_id == user.id,
            TestResult.lesson_id == lesson_id
        ).first()
        
        if existing_result:
            db.delete(existing_result)
        
        # Create new test result
        test_result = TestResult(
            user_id=user.id,
            lesson_id=lesson_id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            passed=passed
        )
        
        db.add(test_result)
        db.commit()
        db.refresh(test_result)
        
        logger.info(f"Test submitted: user {telegram_id}, lesson {lesson_id}, score {score}%")
        
        return {
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "passed": passed,
            "result_id": test_result.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting test for user {telegram_id}, lesson {lesson_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to submit test")

@router.get("/user/{telegram_id}/results")
async def get_user_results(telegram_id: int, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """Get user test results"""
    try:
        # Get user
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get results
        query = db.query(TestResult, Lesson).join(Lesson).filter(TestResult.user_id == user.id)
        
        if limit:
            query = query.limit(limit)
        
        results = query.all()
        
        result_list = []
        for test_result, lesson in results:
            result_data = {
                "id": test_result.id,
                "lesson_title": lesson.title,
                "score": test_result.score,
                "correct_answers": test_result.correct_answers,
                "total_questions": test_result.total_questions,
                "passed": test_result.passed,
                "completed_at": test_result.created_at.isoformat()
            }
            result_list.append(result_data)
        
        return result_list
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting results for user {telegram_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get results")

@router.get("/user/{telegram_id}/stats")
async def get_user_stats(telegram_id: int, db: Session = Depends(get_db)):
    """Get user statistics"""
    try:
        # Get user
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get stats
        total_tests = db.query(TestResult).filter(TestResult.user_id == user.id).count()
        passed_tests = db.query(TestResult).filter(
            TestResult.user_id == user.id,
            TestResult.passed == True
        ).count()
        
        # Calculate average score
        results = db.query(TestResult).filter(TestResult.user_id == user.id).all()
        average_score = sum(r.score for r in results) / len(results) if results else 0
        
        return {
            "phone": user.phone_number,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "average_score": round(average_score, 1),
            "registration_date": user.created_at.strftime("%d.%m.%Y") if user.created_at else "Noma'lum"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats for user {telegram_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user stats")

@router.get("/user/{telegram_id}/progress")
async def get_user_progress(telegram_id: int, db: Session = Depends(get_db)):
    """Get user learning progress"""
    try:
        # Get user
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get progress data
        total_lessons = db.query(Lesson).count()
        accessible_lessons = db.query(Access).filter(Access.user_id == user.id).count()
        completed_lessons = db.query(TestResult).filter(
            TestResult.user_id == user.id,
            TestResult.passed == True
        ).count()
        
        total_tests = db.query(TestResult).filter(TestResult.user_id == user.id).count()
        passed_tests = db.query(TestResult).filter(
            TestResult.user_id == user.id,
            TestResult.passed == True
        ).count()
        
        results = db.query(TestResult).filter(TestResult.user_id == user.id).all()
        average_score = sum(r.score for r in results) / len(results) if results else 0
        
        # Get last test date
        last_result = db.query(TestResult).filter(TestResult.user_id == user.id).order_by(TestResult.created_at.desc()).first()
        last_test_date = last_result.created_at.strftime("%d.%m.%Y") if last_result else "Hali yo'q"
        
        return {
            "total_lessons": total_lessons,
            "accessible_lessons": accessible_lessons,
            "completed_lessons": completed_lessons,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "average_score": round(average_score, 1),
            "last_test_date": last_test_date,
            "last_login": "Bugun"  # Could track this separately
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting progress for user {telegram_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user progress")

@router.get("/user/{telegram_id}/result/{result_id}")
async def get_result_detail(telegram_id: int, result_id: int, db: Session = Depends(get_db)):
    """Get detailed test result"""
    try:
        # Get user
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get result
        result = db.query(TestResult, Lesson).join(Lesson).filter(
            TestResult.id == result_id,
            TestResult.user_id == user.id
        ).first()
        
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        
        test_result, lesson = result
        
        # For now, return basic result info
        # In a full implementation, you'd store individual answer details
        return {
            "lesson_title": lesson.title,
            "score": test_result.score,
            "correct_answers": test_result.correct_answers,
            "total_questions": test_result.total_questions,
            "completed_at": test_result.created_at.isoformat(),
            "answers": []  # Would contain individual answers if stored
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting result detail for user {telegram_id}, result {result_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get result detail")