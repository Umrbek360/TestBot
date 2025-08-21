import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from user_manager import UserManager
from test_manager import TestManager

# Initialize managers
user_manager = UserManager()
test_manager = TestManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_manager.register_user(user.id, user.first_name or "Foydalanuvchi")
    
    keyboard = [
        [InlineKeyboardButton("📝 Test ishlash", callback_data="test")],
        [InlineKeyboardButton("👤 Mening hisobim", callback_data="account")],
        [InlineKeyboardButton("⚙️ Akkountim", callback_data="admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Salom {user.first_name}! Hush kelibsiz! 🎓\n\n"
        "Test tizimiga xush kelibsiz. Quyidagi tugmalardan birini tanlang:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle main menu button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "test":
        await show_subjects(query)
    elif query.data == "account":
        await show_account_info(query)
    elif query.data == "admin":
        await show_admin_panel(query)

async def show_subjects(query) -> None:
    """Show available subjects for testing."""
    subjects = test_manager.get_subjects()
    keyboard = []
    
    for subject_id, subject_name in subjects.items():
        keyboard.append([InlineKeyboardButton(
            f"📚 {subject_name}", 
            callback_data=f"test_{subject_id}"
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "Fanlardan birini tanlang:",
        reply_markup=reply_markup
    )

async def test_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle subject selection and start test."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_main":
        await back_to_main(query)
        return
    
    subject_id = query.data.replace("test_", "")
    user_id = query.from_user.id
    
    # Start new test session
    test_manager.start_test(user_id, subject_id)
    
    await show_question(query, user_id, subject_id, 0)

async def show_question(query, user_id: int, subject_id: str, question_index: int) -> None:
    """Display current question with answer options."""
    question_data = test_manager.get_question(subject_id, question_index)
    
    if not question_data:
        await end_test(query, user_id, subject_id)
        return
    
    question_text = question_data["question"]
    options = question_data["options"]
    
    keyboard = []
    for i, option in enumerate(options):
        keyboard.append([InlineKeyboardButton(
            f"{chr(65+i)}) {option}", 
            callback_data=f"answer_{subject_id}_{question_index}_{i}"
        )])
    
    progress = f"Savol {question_index + 1}/10"
    subject_name = test_manager.get_subjects()[subject_id]
    
    await query.edit_message_text(
        f"📚 {subject_name}\n{progress}\n\n"
        f"❓ {question_text}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user answers."""
    query = update.callback_query
    await query.answer()
    
    # Parse callback data: answer_subject_question_option
    parts = query.data.split("_")
    subject_id = parts[1]
    question_index = int(parts[2])
    selected_option = int(parts[3])
    
    user_id = query.from_user.id
    
    # Record answer
    test_manager.record_answer(user_id, subject_id, question_index, selected_option)
    
    # Show next question or end test
    next_question = question_index + 1
    if next_question < 10:
        await show_question(query, user_id, subject_id, next_question)
    else:
        await end_test(query, user_id, subject_id)

async def end_test(query, user_id: int, subject_id: str) -> None:
    """End test and show results."""
    results = test_manager.calculate_results(user_id, subject_id)
    user_manager.save_test_result(user_id, subject_id, results)
    
    subject_name = test_manager.get_subjects()[subject_id]
    correct = results["correct"]
    total = results["total"]
    percentage = results["percentage"]
    
    keyboard = [
        [InlineKeyboardButton("📊 Boshqa test", callback_data="test")],
        [InlineKeyboardButton("👤 Natijalarim", callback_data="account")],
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"✅ Test yakunlandi!\n\n"
        f"📚 Fan: {subject_name}\n"
        f"✔️ To'g'ri javoblar: {correct}/{total}\n"
        f"❌ Noto'g'ri javoblar: {total - correct}/{total}\n"
        f"📈 Natija: {percentage:.1f}%\n\n"
        f"{'🎉 Ajoyib!' if percentage >= 80 else '💪 Yaxshi!' if percentage >= 60 else '📚 Koproq mashq qiling!'}",
        reply_markup=reply_markup
    )

async def show_account_info(query) -> None:
    """Show user's account information and test history."""
    user_id = query.from_user.id
    user_data = user_manager.get_user_data(user_id)
    
    if not user_data or not user_data.get("test_history"):
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📊 Hali hech qanday test topshirmadingiz.\n\n"
            "Test ishlash uchun bosh menyuga qayting.",
            reply_markup=reply_markup
        )
        return
    
    # Calculate overall statistics
    subjects = test_manager.get_subjects()
    stats_text = f"👤 {user_data['name']}\n\n📈 Test natijalari:\n\n"
    
    total_tests = 0
    total_correct = 0
    total_questions = 0
    
    for subject_id, results_list in user_data["test_history"].items():
        if results_list:
            subject_name = subjects.get(subject_id, f"Fan {subject_id}")
            latest_result = results_list[-1]
            
            stats_text += f"📚 {subject_name}:\n"
            stats_text += f"   ✔️ To'g'ri: {latest_result['correct']}/10\n"
            stats_text += f"   📊 Foiz: {latest_result['percentage']:.1f}%\n"
            stats_text += f"   📅 Testlar soni: {len(results_list)}\n\n"
            
            total_tests += len(results_list)
            total_correct += latest_result['correct']
            total_questions += latest_result['total']
    
    if total_questions > 0:
        overall_percentage = (total_correct / total_questions) * 100
        stats_text += f"🎯 Umumiy natija: {overall_percentage:.1f}%\n"
        stats_text += f"📊 Jami testlar: {total_tests}"
    
    keyboard = [
        [InlineKeyboardButton("🔄 Yangi test", callback_data="test")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(stats_text, reply_markup=reply_markup)

async def show_admin_panel(query) -> None:
    """Show admin/account management panel."""
    keyboard = [
        [InlineKeyboardButton("🗑️ Natijalarni tozalash", callback_data="admin_clear")],
        [InlineKeyboardButton("📊 Batafsil statistika", callback_data="admin_stats")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⚙️ Akkount boshqaruvi\n\n"
        "Quyidagi amallardan birini tanlang:",
        reply_markup=reply_markup
    )

async def account_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle account-related actions."""
    query = update.callback_query
    await query.answer()
    
    # Handle account actions here if needed
    await back_to_main(query)

async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin panel actions."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == "admin_clear":
        user_manager.clear_user_history(user_id)
        await query.edit_message_text(
            "✅ Barcha natijalar tozalandi!\n\n"
            "Yangi testlarni boshlashingiz mumkin.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Bosh menyu", callback_data="back_main")
            ]])
        )
    elif query.data == "admin_stats":
        await show_detailed_stats(query, user_id)
    else:
        await back_to_main(query)

async def show_detailed_stats(query, user_id: int) -> None:
    """Show detailed user statistics."""
    user_data = user_manager.get_user_data(user_id)
    
    if not user_data or not user_data.get("test_history"):
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="admin")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📊 Statistika mavjud emas.\n\n"
            "Avval test ishlang.",
            reply_markup=reply_markup
        )
        return
    
    subjects = test_manager.get_subjects()
    stats_text = "📈 Batafsil statistika:\n\n"
    
    for subject_id, results_list in user_data["test_history"].items():
        if results_list:
            subject_name = subjects.get(subject_id, f"Fan {subject_id}")
            stats_text += f"📚 {subject_name}:\n"
            
            total_attempts = len(results_list)
            avg_percentage = sum(r['percentage'] for r in results_list) / total_attempts
            best_score = max(r['percentage'] for r in results_list)
            
            stats_text += f"   🔢 Urinishlar: {total_attempts}\n"
            stats_text += f"   📊 O'rtacha: {avg_percentage:.1f}%\n"
            stats_text += f"   🏆 Eng yaxshi: {best_score:.1f}%\n\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Akkount", callback_data="admin")],
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(stats_text, reply_markup=reply_markup)

async def back_to_main(query) -> None:
    """Return to main menu."""
    keyboard = [
        [InlineKeyboardButton("📝 Test ishlash", callback_data="test")],
        [InlineKeyboardButton("👤 Mening hisobim", callback_data="account")],
        [InlineKeyboardButton("⚙️ Akkountim", callback_data="admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🏠 Bosh menyu\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=reply_markup
    )
