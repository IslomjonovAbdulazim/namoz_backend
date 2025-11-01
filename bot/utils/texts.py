# Uzbek text constants for the bot

class BotTexts:
    # Welcome messages
    WELCOME = "👋 Xush kelibsiz, {name}!\n\n🎓 Bu bot darslarni o'rganish uchun mo'ljallangan.\n\nBot bilan ishlash uchun telefon raqamingizni baham ko'rish kerak."
    WELCOME_REGISTERED = "👋 Xush kelibsiz, {name}!\n\n🎓 Bu bot darslarni o'rganish uchun mo'ljallangan.\n\nQuyidagi tugmalar orqali botdan foydalanishingiz mumkin:"
    
    # Phone registration
    PHONE_REQUEST = "📱 Botdan foydalanish uchun telefon raqamingizni baham ko'ring.\n\nBuning uchun quyidagi tugmani bosing:"
    PHONE_RECEIVED = "✅ Telefon raqamingiz qabul qilindi!\n\nEndi botdan to'liq foydalanishingiz mumkin."
    PHONE_ERROR = "❌ Telefon raqamini baham ko'rishda xatolik yuz berdi. Qaytadan urinib ko'ring."
    
    # Main menu
    MY_LESSONS = "📚 Mening darslarim"
    MY_RESULTS = "📊 Natijalarim"
    PROFILE = "👤 Profil"
    HELP = "❓ Yordam"
    SETTINGS = "⚙️ Sozlamalar"
    MAIN_MENU = "🏠 Asosiy menyu"
    BACK_TO_LESSONS = "🔙 Darslarga qaytish"
    REFRESH = "🔄 Yangilash"
    
    # Quick actions
    QUICK_LESSONS = "⚡ Tez darslar"
    LATEST_RESULTS = "🆕 So'nggi natijalar"
    PROGRESS = "📈 Taraqqiyot"
    
    # Lessons
    LESSONS_LIST = "📚 **Darslar ro'yxati:**\n\n"
    NO_LESSONS = "📚 Hozircha darslar mavjud emas."
    LESSONS_ERROR = "❌ Darslarni yuklashda xatolik. Keyinroq qaytadan urinib ko'ring."
    LESSON_NOT_FOUND = "❌ Dars topilmadi."
    
    # Lesson access
    LOCKED_LESSON = "🔒 **{title}**\n\n📝 {description}\n\n❌ Bu darsga kirish huquqingiz yo'q.\n💳 Xarid qilish uchun administrator bilan bog'laning: @Ekolingvist1"
    UNLOCKED_LESSON = "✅ **{title}**\n\n📝 {description}\n\n"
    TEST_COMPLETED = "📊 Test topshirilgan: {score}%\n\n"
    TEST_NOT_COMPLETED = "❓ Test hali topshirilmagan\n\n"
    LESSON_MATERIALS = "📎 **Materiallar:**"
    
    # Materials
    VIDEO = "🎥 Video"
    PDF = "📄 PDF"
    PRESENTATION = "📊 Taqdimot"
    
    # Test
    TAKE_TEST = "❓ Test topshirish"
    VIEW_RESULT = "📊 Natijani ko'rish"
    TEST_ERROR = "❌ Test savollarini yuklashda xatolik."
    QUESTION_HEADER = "❓ **Savol {current} dan {total}**\n\n{question}\n\n{options}\n\n📝 To'g'ri javobni tanlang:"
    CANCEL_TEST = "❌ Testni bekor qilish"
    
    # Test results
    TEST_FINISHED = "🎉 **Test yakunlandi!**\n\n📊 Sizning natijangiz: {score}%\n✅ To'g'ri javoblar: {correct} ta {total} tadan\n\n"
    TEST_PASSED = "🎊 Tabriklaymiz! Testni muvaffaqiyatli topshirdingiz!"
    TEST_FAILED = "😔 Afsuski, test topshirilmadi. Yana urinib ko'ring!"
    TEST_SAVE_ERROR = "❌ Test natijalarini saqlashda xatolik."
    
    # Results
    NO_RESULTS = "📊 Sizda hali test natijalari yo'q."
    RESULTS_LIST = "📊 **Sizning natijalaringiz:**\n\n"
    RESULTS_ERROR = "❌ Natijalarni yuklashda xatolik."
    RESULT_NOT_FOUND = "❌ Natija topilmadi."
    
    # Result details
    RESULT_DETAIL = "📊 **Batafsil natija**\n\n📚 Dars: {lesson}\n🎯 Natija: {score}% ({correct}/{total})\n📅 Sana: {date}\n\n**Javoblar:**\n"
    BACK_TO_RESULTS = "🔙 Natijalarga qaytish"
    
    # Help and info
    HELP_TEXT = """🤖 **Bot haqida ma'lumot:**

📚 **Asosiy funksiyalar:**
• Darslarni ko'rish va o'rganish
• Testlar topshirish va natijalarni ko'rish
• Taraqqiyotni kuzatish

🎯 **Buyruqlar:**
/start - Botni ishga tushirish
/lessons - Darslar ro'yxati
/results - Test natijalari
/help - Yordam

💡 **Maslahatlar:**
• Tugmalar orqali oson navigatsiya qiling
• Testlarni diqqat bilan bajaring
• Natijalardagi tahlillarni ko'rib chiqing

📞 **Yordam kerakmi?**
Administrator bilan bog'laning: @Ekolingvist1"""

    PROFILE_TEXT = """👤 **Sizning profilingiz:**

📱 Telefon: {phone}
📊 Umumiy testlar: {total_tests}
✅ O'tgan testlar: {passed_tests}
📈 O'rtacha ball: {average_score}%
📅 Ro'yxatdan o'tgan: {registration_date}"""

    # Commands
    CMD_LESSONS = "📚 /lessons - Darslar ro'yxati"
    CMD_RESULTS = "📊 /results - Test natijalari"
    CMD_HELP = "❓ /help - Yordam va ma'lumot"
    
    # Errors
    GENERAL_ERROR = "❌ Xatolik yuz berdi. Qaytadan urinib ko'ring yoki administrator bilan bog'laning."
    API_ERROR = "❌ Server bilan bog'lanishda xatolik. Keyinroq qaytadan urinib ko'ring."
    
    # Success indicators
    CORRECT_ANSWER = "✅"
    WRONG_ANSWER = "❌"
    LOCKED_ICON = "🔒"
    UNLOCKED_ICON = "✅"
    
    # Score indicators
    HIGH_SCORE = "🟢"  # 70%+
    MEDIUM_SCORE = "🟡"  # 50-69%
    LOW_SCORE = "🔴"    # <50%
    
    @staticmethod
    def get_score_icon(score: int) -> str:
        if score >= 70:
            return BotTexts.HIGH_SCORE
        elif score >= 50:
            return BotTexts.MEDIUM_SCORE
        else:
            return BotTexts.LOW_SCORE
    
    @staticmethod
    def format_lesson_title(title: str, has_access: bool, score: int = None, price: int = None) -> str:
        icon = BotTexts.UNLOCKED_ICON if has_access else BotTexts.LOCKED_ICON
        
        if has_access and score is not None:
            return f"{icon} {title} ({score}%)"
        elif not has_access and price:
            return f"{icon} {title} - {price:,} so'm"
        else:
            return f"{icon} {title}"