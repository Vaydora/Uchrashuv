from telegram import Update
from telegram.ext import ContextTypes
from keyboards import rules_keyboard, available_dates_keyboard, time_keyboard
from config import ADMIN_ID

questions = [
    "👤 Kimni kutyapsiz?",
    "✍️ Ism:",
    "💼 Kasb:",
    "🎯 Uchrashuv maqsadi:",
    "💬 Suhbat mavzulari:",
    "📍 Manzil:",
    "🎭 Obraz:"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌟 *Salom! Men Bob, sizning shaxsiy uchrashuv maslahatchingiz.*\n\n"
        "📅 Uchrashuv buyurtmasini berish uchun davom eting."
    )
    await update.message.reply_text(welcome_text)

async def accept_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 Uchrashuv qoidalari:", reply_markup=rules_keyboard())

async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Iltimos uchrashuv kunini tanlang:", reply_markup=available_dates_keyboard())

async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_date = context.user_data.get('selected_date')
    keyboard = time_keyboard()
    await query.message.reply_text(f"⏰ {selected_date} uchun vaqtni tanlang:", reply_markup=keyboard)

async def handle_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'q_index' not in context.user_data:
        context.user_data['q_index'] = 0
        context.user_data['survey'] = {}
    q_index = context.user_data['q_index']
    context.user_data['survey'][q_index] = update.message.text
    q_index += 1
    if q_index < len(questions):
        context.user_data['q_index'] = q_index
        await update.message.reply_text(questions[q_index])
    else:
        context.user_data['q_index'] = None
        await update.message.reply_text("👧 Iltimos, qizning ismini kiriting:")
        context.user_data['ask_name'] = True

async def save_obraz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('ask_name'):
        context.user_data['ask_name'] = False
        context.user_data['girl_name'] = update.message.text
        await update.message.reply_text("🔖 Tanib olish uchun belgini yozing yoki rasm jo‘nating:")
        context.user_data['ask_sign'] = True
    elif context.user_data.get('ask_sign'):
        context.user_data['ask_sign'] = False
        if update.message.photo:
            context.user_data['sign'] = "Rasm yuborildi"
        else:
            context.user_data['sign'] = update.message.text
        # Adminga yuborish
        survey_data = context.user_data.get('survey', {})
        msg = "📝 Yangi buyurtma va anketa:\n"
        for i, answer in enumerate(survey_data.values()):
            msg += f"{questions[i]} {answer}\n"
        msg += f"👧 Qiz ismi: {context.user_data['girl_name']}\n"
        msg += f"🔖 Tanib olish belgisi / rasm: {context.user_data['sign']}\n"
        msg += f"📅 Uchrashuv kuni: {context.user_data.get('selected_date')}\n"
        msg += f"⏰ Vaqti: {context.user_data.get('selected_time')}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        await update.message.reply_text("✅ Anketa to‘ldirildi va adminga yuborildi.")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("Admin panel ishlayapti")
