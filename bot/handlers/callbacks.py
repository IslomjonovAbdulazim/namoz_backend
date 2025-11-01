import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from bot.services.user_service import UserService
from bot.services.api_client import APIClient
from bot.utils.texts import BotTexts
from bot.utils.helpers import get_user_display_name, format_date, calculate_correct_answers
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.keyboards.lessons import (
    get_lessons_list_keyboard, 
    get_lesson_materials_keyboard,
    get_test_question_keyboard,
    get_test_finished_keyboard
)
from bot.keyboards.results import get_results_list_keyboard, get_result_detail_keyboard

logger = logging.getLogger(__name__)

class CallbackHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.api = user_service.api
    
    async def safe_edit_message(self, update: Update, text: str, reply_markup=None, parse_mode="Markdown"):
        """Safely edit message, handling 'message not modified' errors"""
        try:
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
            else:
                await update.message.reply_text(
                    text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
        except BadRequest as e:
            if "message is not modified" in str(e).lower():
                # Message content is the same, just ignore
                logger.debug(f"Message not modified - content is the same")
                return
            else:
                # Other BadRequest errors should be raised
                raise e
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main callback handler"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user = update.effective_user
        
        try:
            if data == "start":
                await self.show_main_menu(update, context)
            elif data == "lessons":
                await self.show_lessons(update, context)
            elif data == "results":
                await self.show_results(update, context)
            elif data == "help":
                await self.show_help(update, context)
            elif data == "profile":
                await self.show_profile(update, context)
            elif data == "quick_lessons":
                await self.show_quick_lessons(update, context)
            elif data == "progress":
                await self.show_progress(update, context)
            elif data == "latest_results":
                await self.show_latest_results(update, context)
            elif data == "refresh_data":
                await self.refresh_data(update, context)
            elif data.startswith("lesson_"):
                lesson_id = data.split("_", 1)[1]
                await self.show_lesson_detail(update, context, lesson_id)
            elif data.startswith("test_"):
                lesson_id = data.split("_", 1)[1]
                await self.start_test(update, context, lesson_id)
            elif data.startswith("answer_"):
                parts = data.split("_")
                question_id = parts[1]
                answer_idx = int(parts[2])
                await self.handle_answer(update, context, question_id, answer_idx)
            elif data.startswith("result_detail_"):
                result_id = data.split("_", 2)[2]
                await self.show_result_detail(update, context, result_id)
            elif data.startswith("test_result_"):
                lesson_id = data.split("_", 2)[2]
                await self.show_lesson_test_result(update, context, lesson_id)
                
        except Exception as e:
            logger.error(f"Error handling callback {data} for user {user.id}: {e}")
            await query.edit_message_text(BotTexts.GENERAL_ERROR)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main menu"""
        user = update.effective_user
        welcome_text = BotTexts.WELCOME_REGISTERED.format(name=get_user_display_name(user))
        
        await self.safe_edit_message(update, welcome_text, get_main_menu_keyboard(), "Markdown")
    
    async def show_lessons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show lessons list"""
        user = update.effective_user
        lessons_data = await self.user_service.get_user_lessons(user.id)
        
        if lessons_data is None:
            text = BotTexts.LESSONS_ERROR
            keyboard = get_main_menu_keyboard()
        elif not lessons_data:
            text = BotTexts.NO_LESSONS
            keyboard = get_main_menu_keyboard()
        else:
            text = BotTexts.LESSONS_LIST
            for lesson in lessons_data:
                status_line = BotTexts.format_lesson_title(
                    lesson['title'], 
                    lesson['has_access'], 
                    lesson.get('score'), 
                    lesson.get('price')
                )
                text += f"{status_line}\n"
            
            keyboard = get_lessons_list_keyboard(lessons_data)
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
    
    async def show_lesson_detail(self, update: Update, context: ContextTypes.DEFAULT_TYPE, lesson_id: str):
        """Show lesson details"""
        user = update.effective_user
        lesson_data = await self.user_service.get_lesson_detail(user.id, lesson_id)
        
        if not lesson_data:
            await self.safe_edit_message(update,BotTexts.LESSON_NOT_FOUND)
            return
        
        if not lesson_data["has_access"]:
            text = BotTexts.LOCKED_LESSON.format(
                title=lesson_data['title'],
                description=lesson_data['description']
            )
            keyboard = get_lessons_list_keyboard([])  # Empty list for back button only
        else:
            text = BotTexts.UNLOCKED_LESSON.format(
                title=lesson_data['title'],
                description=lesson_data['description']
            )
            
            if lesson_data.get("test_completed"):
                text += BotTexts.TEST_COMPLETED.format(score=lesson_data.get('score', 0))
            else:
                text += BotTexts.TEST_NOT_COMPLETED
            
            text += BotTexts.LESSON_MATERIALS
            
            keyboard = get_lesson_materials_keyboard(
                lesson_data, 
                lesson_id, 
                lesson_data.get("test_completed", False)
            )
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
    
    async def start_test(self, update: Update, context: ContextTypes.DEFAULT_TYPE, lesson_id: str):
        """Start test for lesson"""
        user = update.effective_user
        questions_data = await self.api.get_lesson_questions(user.id, lesson_id)
        
        if not questions_data:
            await self.safe_edit_message(update,BotTexts.TEST_ERROR)
            return
        
        # Store test data in context
        context.user_data["test_questions"] = questions_data
        context.user_data["test_answers"] = []
        context.user_data["current_question"] = 0
        context.user_data["lesson_id"] = lesson_id
        
        await self.show_question(update, context)
    
    async def show_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current test question"""
        questions = context.user_data.get("test_questions", [])
        current_idx = context.user_data.get("current_question", 0)
        
        if current_idx >= len(questions):
            await self.finish_test(update, context)
            return
        
        question = questions[current_idx]
        text = BotTexts.QUESTION_HEADER.format(
            current=current_idx + 1,
            total=len(questions),
            question=question['question_text']
        )
        
        keyboard = get_test_question_keyboard(
            question['id'], 
            question["options"], 
            context.user_data['lesson_id']
        )
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE, question_id: str, answer_idx: int):
        """Handle test answer"""
        answers = context.user_data.get("test_answers", [])
        answers.append({
            "question_id": question_id,
            "selected_option": answer_idx
        })
        context.user_data["test_answers"] = answers
        context.user_data["current_question"] = context.user_data.get("current_question", 0) + 1
        
        await self.show_question(update, context)
    
    async def finish_test(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Finish test and show results"""
        user = update.effective_user
        lesson_id = context.user_data.get("lesson_id")
        answers = context.user_data.get("test_answers", [])
        
        result_data = await self.api.submit_test(user.id, lesson_id, answers)
        
        if not result_data:
            await self.safe_edit_message(update,BotTexts.TEST_SAVE_ERROR)
            return
        
        correct_answers = calculate_correct_answers(result_data['score'], result_data['total_questions'])
        
        text = BotTexts.TEST_FINISHED.format(
            score=result_data['score'],
            correct=correct_answers,
            total=result_data['total_questions']
        )
        
        if result_data.get("passed"):
            text += BotTexts.TEST_PASSED
        else:
            text += BotTexts.TEST_FAILED
        
        keyboard = get_test_finished_keyboard()
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
        
        # Clear test data
        context.user_data.clear()
    
    async def show_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user results"""
        user = update.effective_user
        results_data = await self.user_service.get_user_results(user.id)
        
        if results_data is None:
            text = BotTexts.RESULTS_ERROR
            keyboard = get_main_menu_keyboard()
        elif not results_data:
            text = BotTexts.NO_RESULTS
            keyboard = get_results_list_keyboard([])
        else:
            text = BotTexts.RESULTS_LIST
            for result in results_data:
                score_icon = BotTexts.get_score_icon(result["score"])
                text += f"{score_icon} {result['lesson_title']}: {result['score']}%\n"
            
            keyboard = get_results_list_keyboard(results_data)
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
    
    async def show_result_detail(self, update: Update, context: ContextTypes.DEFAULT_TYPE, result_id: str):
        """Show detailed test result"""
        user = update.effective_user
        result_data = await self.api.get_result_detail(user.id, result_id)
        
        if not result_data:
            await self.safe_edit_message(update,BotTexts.RESULT_NOT_FOUND)
            return
        
        correct_answers = calculate_correct_answers(result_data['score'], result_data['total_questions'])
        
        text = BotTexts.RESULT_DETAIL.format(
            lesson=result_data['lesson_title'],
            score=result_data['score'],
            correct=correct_answers,
            total=result_data['total_questions'],
            date=format_date(result_data['completed_at'])
        )
        
        # Add answers details
        for i, answer in enumerate(result_data.get("answers", []), 1):
            icon = BotTexts.CORRECT_ANSWER if answer["is_correct"] else BotTexts.WRONG_ANSWER
            text += f"{i}. {icon} {answer['question'][:50]}...\n"
        
        keyboard = get_result_detail_keyboard()
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
    
    async def show_lesson_test_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE, lesson_id: str):
        """Show test result for specific lesson"""
        # This would need to find the result_id for the given lesson
        # For now, redirect to general results
        await self.show_results(update, context)
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        from bot.keyboards.main_menu import get_back_to_main_keyboard
        
        await self.safe_edit_message(
            update, 
            BotTexts.HELP_TEXT,
            get_back_to_main_keyboard(),
            "Markdown"
        )
    
    async def show_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user profile information"""
        from bot.keyboards.main_menu import get_back_to_main_keyboard
        
        user = update.effective_user
        user_stats = await self.user_service.get_user_stats(user.id)
        
        if user_stats:
            text = BotTexts.PROFILE_TEXT.format(
                phone=user_stats.get('phone', 'Kiritilmagan'),
                total_tests=user_stats.get('total_tests', 0),
                passed_tests=user_stats.get('passed_tests', 0),
                average_score=user_stats.get('average_score', 0),
                registration_date=user_stats.get('registration_date', 'Noma\'lum')
            )
        else:
            text = "❌ Profil ma'lumotlarini yuklashda xatolik yuz berdi."
        
        await self.safe_edit_message(update, text, get_back_to_main_keyboard(), "Markdown")
    
    async def show_quick_lessons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show quick access to recent or recommended lessons"""
        user = update.effective_user
        lessons_data = await self.user_service.get_user_lessons(user.id)
        
        if not lessons_data:
            text = "📚 Hozircha mavjud darslar yo'q yoki ularga kirish huquqingiz yo'q."
            keyboard = get_main_menu_keyboard()
        else:
            # Show only accessible lessons
            accessible_lessons = [lesson for lesson in lessons_data if lesson.get('has_access', False)]
            
            if not accessible_lessons:
                text = "🔒 Sizda hali ochiq darslar yo'q. Darslarni sotib oling yoki administrator bilan bog'laning."
                keyboard = get_main_menu_keyboard()
            else:
                text = "⚡ **Tez darslar:**\n\n"
                for lesson in accessible_lessons[:5]:  # Show first 5 accessible lessons
                    status = "✅ Bajarilgan" if lesson.get('score') else "❓ Bajarilmagan"
                    text += f"📚 {lesson['title']} - {status}\n"
                
                keyboard = get_lessons_list_keyboard(accessible_lessons[:5])
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
    
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user learning progress"""
        from bot.keyboards.main_menu import get_back_to_main_keyboard
        
        user = update.effective_user
        progress_data = await self.user_service.get_user_progress(user.id)
        
        if progress_data:
            text = f"""📈 **Sizning taraqqiyotingiz:**

📊 **Umumiy statistika:**
• Jami darslar: {progress_data.get('total_lessons', 0)}
• Ochiq darslar: {progress_data.get('accessible_lessons', 0)}
• Yakunlangan darslar: {progress_data.get('completed_lessons', 0)}

🎯 **Test natijalari:**
• Topshirilgan testlar: {progress_data.get('total_tests', 0)}
• Muvaffaqiyatli: {progress_data.get('passed_tests', 0)}
• O'rtacha ball: {progress_data.get('average_score', 0)}%

📅 **So'nggi faollik:**
• Oxirgi test: {progress_data.get('last_test_date', 'Hali yo\'q')}
• Oxirgi kirish: {progress_data.get('last_login', 'Noma\'lum')}"""
        else:
            text = "❌ Taraqqiyot ma'lumotlarini yuklashda xatolik yuz berdi."
        
        await self.safe_edit_message(update, text, get_back_to_main_keyboard(), "Markdown")
    
    async def show_latest_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show latest test results"""
        user = update.effective_user
        results_data = await self.user_service.get_user_results(user.id, limit=5)
        
        if not results_data:
            text = "📊 So'nggi natijalar mavjud emas."
            keyboard = get_main_menu_keyboard()
        else:
            text = "🆕 **So'nggi 5 ta natija:**\n\n"
            for result in results_data:
                score_icon = BotTexts.get_score_icon(result["score"])
                text += f"{score_icon} {result['lesson_title']}: {result['score']}%\n"
            
            keyboard = get_results_list_keyboard(results_data)
        
        await self.safe_edit_message(update, text, keyboard, "Markdown")
    
    async def refresh_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Refresh user data and show main menu"""
        await self.safe_edit_message(update, "🔄 Ma'lumotlar yangilanmoqda...", None, "Markdown")
        
        # Small delay to show loading message
        import asyncio
        await asyncio.sleep(1)
        
        # Clear any cached data if your service has caching
        # await self.user_service.clear_cache(user.id)
        
        await self.show_main_menu(update, context)