from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import date, timedelta

# ==========================
# BOT SOZLAMALARI
# ==========================
BOT_TOKEN = "8493748950:AAFuBvXYDc4H4tA5pWcopl317BtxRlS5aNs"  # BotFather dan olingan token
ADMIN_ID = 6603473829  # o'zingizning admin ID

busy_dates = ["2025-08-27", "2025-08-29"]  # Band kunlar
questions = [
    "👤 Kimni kutyapsiz?",
    "✍️ Ism:",
    "💼 Kasb:",
    "🎯 Uchrashuv maqsadi:",
    "💬 Suhbat mavzulari:",
    "📍 Manzil:",
    "🎭 Obraz:"
]

# ==========================
# START
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌟 *Salom! Men Bob, sizning shaxsiy uchrashuv maslahatchingiz.*\n\n"
        "📅 Uchrashuv buyurtmasini berish uchun davom eting."
    )
    keyboard = [[InlineKeyboardButton("➡️ Davom etish", callback_data='privacy')]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# ==========================
# INLINE TUGMALAR OQIMI
# ==========================
async def user_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'privacy':
        text = "🔒 *Maxfiylik shartnomasi:*\n\n" \
               "1️⃣ Sizning ma'lumotlaringiz sir saqlanadi.\n" \
               "2️⃣ Uchrashuv tafsilotlari faqat siz va Bob orasida qoladi.\n" \
               "3️⃣ Foydalanuvchi xabarlari xavfsiz saqlanadi.\n" \
               "4️⃣ Nojo‘ya harakatlar aniqlansa, uchrashuv bekor qilinadi."
        keyboard = [[InlineKeyboardButton("✅ Roziman", callback_data='rules')]]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'rules':
        text = "📜 *Uchrashuv qoidalari:* \n\n" \
               "1️⃣ Uchrashuv haqida hech kim bilan gaplashmaslik. \n" \
               "2️⃣ Tafsilotlarni oshkor qilmaslik. \n" \
               "3️⃣ Inson huquqlari va hurmat saqlash zarur. \n" \
               "4️⃣ Har ikki tomon roziligi bo‘lishi kerak. \n" \
               "5️⃣ Har doim harajatlar buyurtmachi tomonidan qoplanadi."
        keyboard = [[InlineKeyboardButton("✅ Qoidalarni qabul qilaman", callback_data='select_date')]]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'select_date':
        keyboard = available_dates_keyboard()
        await query.message.reply_text("📅 Iltimos, uchrashuv kunini tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('date_'):
        selected_date = query.data.split('_')[1]
        context.user_data['selected_date'] = selected_date
        keyboard = [
            [InlineKeyboardButton("🕗 20:00 - 21:00", callback_data='time_20')],
            [InlineKeyboardButton("🕘 21:00 - 22:00", callback_data='time_21')]
        ]
        await query.message.reply_text(f"⏰ {selected_date} uchun vaqtni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('time_'):
        selected_time = query.data.split('_')[1]
        context.user_data['selected_time'] = selected_time
        await query.message.reply_text(f"✅ Siz {context.user_data['selected_date']} kuni {selected_time} vaqti uchun tanladingiz.\n\nAnketa boshlanadi...")
        context.user_data['survey'] = {}
        context.user_data['q_index'] = 0
        await query.message.reply_text(questions[0])

# ==========================
# FOYDALANUVCHI ANKETA
# ==========================
async def handle_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'q_index' in context.user_data:
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

async def handle_name_and_sign(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# ==========================
# FOYDALANUVCHI FOYDALANISHI UCHUN FUNKSIYALAR
# ==========================
def available_dates_keyboard():
    today = date.today()
    keyboard = []
    for i in range(7):
        day = today + timedelta(days=i)
        if str(day) in busy_dates:
            keyboard.append([InlineKeyboardButton(f"{day} ❌ Band", callback_data='busy')])
        else:
            keyboard.append([InlineKeyboardButton(f"{day} ✅ Tanlash", callback_data=f'date_{day}')])
    return keyboard

# ==========================
# BOTNI ISHGA TUSHURISH
# ==========================
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(user_buttons, pattern='.*'))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_survey))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_and_sign))
app.add_handler(MessageHandler(filters.PHOTO, handle_name_and_sign))

print("Bot ishlamoqda...")
app.run_polling()
