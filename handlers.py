from telegram import Update
from telegram.ext import ContextTypes
from keyboards import privacy_keyboard, rules_keyboard, available_dates_keyboard, time_keyboard
from config import ADMIN_ID, questions

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌟 *Salom! Men Bob, sizning shaxsiy uchrashuv maslahatchingiz.*\n\n"
        "📅 Uchrashuv buyurtmasini berish uchun davom eting."
    )
    keyboard = [[InlineKeyboardButton("➡️ Davom etish", callback_data='privacy')]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Maxfiylik shartnomasi
async def accept_privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "🔒 *Maxfiylik shartnomasi:*\n\n" \
           "1️⃣ Sizning ma'lumotlaringiz sir saqlanadi.\n" \
           "2️⃣ Uchrashuv tafsilotlari faqat siz va Bob orasida qoladi.\n" \
           "3️⃣ Foydalanuvchi xabarlari xavfsiz saqlanadi.\n" \
           "4️⃣ Nojo‘ya harakatlar aniqlansa, uchrashuv bekor qilinadi."
    await query.message.reply_text(text, reply_markup=rules_keyboard, parse_mode='Markdown')

# Uchrashuv qoidalari
async def accept_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "📜 *Uchrashuv qoidalari:* \n\n" \
           "1️⃣ Uchrashuv haqida hech kim bilan gaplashmaslik. \n" \
           "2️⃣ Tafsilotlarni oshkor qilmaslik. \n" \
           "3️⃣ Inson huquqlari va hurmat saqlash zarur. \n" \
           "4️⃣ Har ikki tomon roziligi bo‘lishi kerak. \n" \
           "5️⃣ Har doim harajatlar buyurtmachi tomonidan qoplanadi."
    keyboard = [[InlineKeyboardButton("📅 Sanani tanlash", callback_data='select_date')]]
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Sanani tanlash
async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📅 Iltimos, uchrashuv kunini tanlang:", reply_markup=available_dates_keyboard())

# Vaqtni tanlash
async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("⏰ Iltimos, vaqtni tanlang:", reply_markup=time_keyboard)

# Anketa
async def handle_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'q_index' not in context.user_data:
        context.user_data['survey'] = {}
        context.user_data['q_index'] = 0
        await update.message.reply_text(questions[0])
        return

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

# Obraz va ism, belgi/rassm
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

# Admin panel
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = int(data.split('_')[1])
    if data.startswith('approve_'):
        await context.bot.send_message(chat_id=user_id, text="✅ Buyurtmangiz tasdiqlandi!")
        await query.edit_message_text("Buyurtma tasdiqlandi.")
    elif data.startswith('reject_'):
        await context.bot.send_message(chat_id=user_id, text="❌ Buyurtmangiz rad etildi.")
        await query.edit_message_text("Buyurtma rad etildi.")from telegram import Update

