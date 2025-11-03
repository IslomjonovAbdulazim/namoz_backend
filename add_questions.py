#!/usr/bin/env python3
"""
Script to add Uzbek linguistics test questions to the database
"""

import asyncio
import uuid
from sqlalchemy.orm import Session
from app.core.database import get_db, init_db
from app.models.test_question import TestQuestionDB

# Define the questions with their correct answers
QUESTIONS = [
    {
        "question_text": "1. Monografiya so'zida urg'u qaysi bo'g'inga tushgan?",
        "options": ["3-bo'g'in", "1-bo'g'in", "2-bo'g'in", "4-bo'g'in"],
        "correct_option": 0  # A) 3-bo'g'in
    },
    {
        "question_text": "2. Quyida berilgan baytda nechta so'zda ochiq bo'g'in mavjud?\nIlmdan bir shu'la dilga tushgan on,\nAniq bilursankim, ilm bepoyon.",
        "options": ["4 ta", "5 ta", "6 ta", "7 ta"],
        "correct_option": 2  # C) 6 ta
    },
    {
        "question_text": "3. Qaysi so'zlarda nuqtalar o'rniga bo'g'iz undoshi qo'yiladi?",
        "options": ["su…bat, ...il-…il", "no'…at, ...ayot", "ba...t, ogo...", "...il-...il, sho'…"],
        "correct_option": 0  # A) suhbat, g'il-g'il
    },
    {
        "question_text": "4. Quyidagi gapda necha o'rinda ng undoshi qo'llangan?\nTubsiz dengiz dedingizmi, dengiz tengsiz dedingizmi?",
        "options": ["5", "3", "2", "4"],
        "correct_option": 3  # D) 4
    },
    {
        "question_text": "5. Qaysi javobda ikkinchi bo'g'ini unli va jarangli undoshlardan iborat bo'lgan so'zlar berilgan?",
        "options": ["qog'oz, qo'g'irchoq, qalam", "qo'shiq, qovun, qamar", "ko'rsat, qirg'ich, qiymat", "qasam, quloq, quyon"],
        "correct_option": 1  # B) qo'shiq, qovun, qamar
    },
    {
        "question_text": "6. Quyida berilgan gapda nechta so'z tarkibida qator undoshlar ishtirok etgan?\nIlm egallashga harakat qilish har bir mo'min va mo'mina uchun farz.",
        "options": ["2ta", "1ta", "3ta", "4ta"],
        "correct_option": 2  # C) 3ta
    },
    {
        "question_text": "7. Qaysi javobdagi so'zda fonetik hodisa kuzatiladi?",
        "options": ["O'ynab gapirsang ham o'ylab gapir.", "Odob yoshlarni kattalar duosiga sazovor etadi.", "Ne-ne to'siqlarni yengishgan edi.", "Asabiylashmay yuzma-yuz o'tirib, fikrimizni tushuntira olamizmi?"],
        "correct_option": 3  # D) Asabiylashmay - fonetik hodisa
    },
    {
        "question_text": "8. Qaysi javobdagi so'zlarda fonetik hodisa kuzatiladi?",
        "options": ["qiynaldi, sanadi", "ma'naviy, o'ksigan", "yumshoq, foydali", "o'ynovchilardan, bog'ga"],
        "correct_option": 3  # D) o'ynovchilardan, bog'ga
    },
    {
        "question_text": "9. Derazamning oldida bir tup,\nO'rik oppoq bo'lib gulladi. Ushbu gapdagi tagiga chizilgan so'zlarda urg'u qayerga tushadi?",
        "options": ["oppoq va gulladi so'zlarida birinchi bo'g'inga", "oppoq so'zida birinchi, gulladi so'zida ikkinchi bo'g'inga", "oppoq so'zida ikkinchi, gulladi so'zida uchinchi bo'g'inga", "oppoq va gulladi so'zlarida ikkinchi bo'g'inga"],
        "correct_option": 1  # B) oppoq so'zida birinchi, gulladi so'zida ikkinchi bo'g'inga
    },
    {
        "question_text": "10. Qaysi so'zlarda qator kelgan undoshlar til oldi jarangli undoshlardan iborat?",
        "options": ["sabr, hukm, darz", "darz, davr, fayz", "zulm, fayz, farzand", "farzand, darz, ranj"],
        "correct_option": 1  # B) darz, davr, fayz
    },
    {
        "question_text": "11. Qaysi gapda portlovchi undosh sirg'aluvchi undosh singari talaffuz qilinadigan so'z qatnashgan?",
        "options": ["Cho'ntagimga yuz so'm solib ko'chaga yugurdim.", "Devor ustida musicha turibdi.", "To'yxonaga sabzi to'g'ragani chiqdik.", "Oltin o'tda, odam mehnatda bilinadi."],
        "correct_option": 2  # C) To'yxonaga sabzi to'g'ragani chiqdik.
    },
    {
        "question_text": "12. Qaysi qatordagi so'zda sirg'aluvchi jarangli undosh sirg'aluvchi jarangsiz undosh sifatida talaffuz qilinadi?",
        "options": ["Devor ustida musicha turibdi.", "To'yxonaga sabzi to'g'ragani chiqdik.", "Cho'ntagimga yuz so'm solib ko'chaga yugurdim.", "Oltin o'tda, odam mehnatda bilinadi."],
        "correct_option": 2  # C) Cho'ntagimga yuz so'm solib ko'chaga yugurdim.
    },
    {
        "question_text": "13. 1) afg'on; 2) avtomobil; 3) faqir; 4) shafqat; 5) afzal; 6) abgor\nBerilgan so'zlarning qaysilarida jarangsiz undosh jarangli jufti kabi talaffuz qilinadi?",
        "options": ["1,2,3,5,6", "1,3,4,5", "1,4,5", "2,3,6"],
        "correct_option": 1  # B) 1,3,4,5
    },
    {
        "question_text": "14. Hadisi sharifda shunday deyilgan: \"Odamlarga nisbatan yomonligingni to'xtat, shu o'zingga sadaqa bo'ladi\".\nUshbu gapda qo'llangan tovush o'zgarishlarining soni va turi to'g'ri berilgan javobni toping.",
        "options": ["2ta tovush ortishi, 1ta tovush tushishi", "1ta tovush ortishi, 1ta tovush almashishi", "2ta tovush ortishi, 1ta tovush almashishi", "1ta tovush ortishi, 2ta tovush almashishi"],
        "correct_option": 2  # C) 2ta tovush ortishi, 1ta tovush almashishi
    },
    {
        "question_text": "15. Jarangli juftiga ega bo'lgan til orqa undoshi qaysi javobda berilgan?",
        "options": ["g", "k", "ng", "q"],
        "correct_option": 0  # A) g
    }
]

def get_lesson_id():
    """Get the lesson ID to associate questions with"""
    # You can change this to the appropriate lesson ID
    return uuid.UUID("1cd67e6f-c024-44ea-b259-a94a1e3d4211")

def add_questions_to_db():
    """Add questions to database"""
    # Initialize database
    init_db()
    
    # Get database session
    db = next(get_db())
    
    try:
        lesson_id = get_lesson_id()
        
        # Delete existing questions for this lesson (optional)
        existing_questions = db.query(TestQuestionDB).filter(TestQuestionDB.lesson_id == lesson_id).all()
        if existing_questions:
            print(f"Found {len(existing_questions)} existing questions. Deleting them...")
            for q in existing_questions:
                db.delete(q)
            db.commit()
        
        # Add new questions
        print(f"Adding {len(QUESTIONS)} new questions...")
        
        for i, q_data in enumerate(QUESTIONS, 1):
            question = TestQuestionDB(
                lesson_id=lesson_id,
                question_text=q_data["question_text"],
                options=q_data["options"],
                correct_option=q_data["correct_option"]
            )
            
            db.add(question)
            print(f"Added question {i}: {q_data['question_text'][:50]}...")
        
        # Commit all questions
        db.commit()
        print(f"\n✅ Successfully added {len(QUESTIONS)} questions to lesson {lesson_id}")
        
        # Verify questions were added
        total_questions = db.query(TestQuestionDB).filter(TestQuestionDB.lesson_id == lesson_id).count()
        print(f"✅ Total questions for this lesson: {total_questions}")
        
    except Exception as e:
        print(f"❌ Error adding questions: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting to add Uzbek linguistics test questions...")
    add_questions_to_db()
    print("🎉 Done!")