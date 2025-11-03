#!/usr/bin/env python3
"""
Demo script to add a multi-line test question
"""

import asyncio
import uuid
from sqlalchemy.orm import Session
from app.core.database import get_db, init_db
from app.models.test_question import TestQuestionDB

# Multi-line question example
MULTILINE_QUESTION = {
    "question_text": """Quyidagi matnni o'qing va savollarga javob bering:

"Ilm - bu insoniyat taraqqiyotining asosi. U nafaqat bilim beradi, balki aqlni ham rivojlantiradi. Har bir inson o'z hayotida ilm orqali muvaffaqiyatga erishishi mumkin."

Ushbu matnda ilm haqida nima aytilgan?""",
    "options": [
        "Ilm faqat bilim beradi va boshqa hech narsa qilmaydi", 
        "Ilm insoniyat taraqqiyotining asosi va aqlni rivojlantiradi",
        "Ilm faqat muvaffaqiyat uchun kerak",
        "Ilm haqida hech narsa aytilmagan"
    ],
    "correct_option": 1
}

def add_multiline_question():
    """Add a multi-line question to test formatting"""
    init_db()
    db = next(get_db())
    
    try:
        lesson_id = uuid.UUID("1cd67e6f-c024-44ea-b259-a94a1e3d4211")
        
        # Add the multiline question
        question = TestQuestionDB(
            lesson_id=lesson_id,
            question_text=MULTILINE_QUESTION["question_text"],
            options=MULTILINE_QUESTION["options"],
            correct_option=MULTILINE_QUESTION["correct_option"]
        )
        
        db.add(question)
        db.commit()
        
        print("✅ Multi-line question added successfully!")
        print(f"Question text preview:")
        print(MULTILINE_QUESTION["question_text"])
        print(f"\nOptions:")
        for i, option in enumerate(MULTILINE_QUESTION["options"]):
            letter = chr(65 + i)
            print(f"{letter}. {option}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Testing multi-line question formatting...")
    add_multiline_question()
    print("🎉 Done!")