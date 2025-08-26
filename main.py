from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import date, timedelta

# ==========================
# Bot token va admin ID
# ==========================
BOT_TOKEN = "8493748950:AAFuBvXYDc4H4tA5pWcopl317BtxRlS5aNs"
ADMIN_ID = 6603473829

# ==========================
# Band kunlar
# ==========================
busy_dates = ["2025-08-27", "2025-08-29"]

# ==========================
# Anketa savollari
# ==========================
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
# /start
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌟 *Salom! Men Bob, sizning shaxsiy uchrashuv maslahatchingiz.*\n\n"
        "📅 Uchrashuv buyurtmasini berish uchun davom eting."
    )
    keyboard = [[InlineKeyboardButton("➡️ Davom etish", callback_data='privacy')]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# ==========================
# Inline tugmalar
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

    elif query.data.startswith('cancel'):
        await query.edit_message_text("❌ Jarayon bekor qilindi.")

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
# Sanalarni chiqarish
# ==========================
def get_available_dates():
    today = date.today()
    dates = []
    for i in range(7):  # keyingi 7 kun
        day = today + timedelta(days=i)
        if str(day) in busy_dates:
            dates.append(InlineKeyboardButton(f"{day} ❌ Band", callback_data='busy'))
        else:
            dates.append(InlineKeyboardButton(f"{day} ✅ Tanlash", callback_data=f'date_{day}'))
    return dates

# ==========================
# Anketa savollarini qabul qilish
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

# ==========================
# Qiz ismi va belgisi/rassm
# ==========================
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
# Admin paneli
# ==========================
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
        await query.edit_message_text("Buyurtma rad etildi.")
    elif data.startswith('edit_'):
        await query.edit_message_text("Admin: Iltimos, foydalanuvchiga yuboriladigan matnni yozing.")
        context.user_data['edit_user'] = user_id
    elif data.startswith('addbtn_'):
        await query.edit_message_text("Admin: Iltimos, yangi tugma nomi va matnini yozing (format: Tugma nomi | Xabar).")
        context.user_data['btn_user'] = user_id

async def admin_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if 'edit_user' in context.user_data:
        user_id = context.user_data.pop('edit_user')
        await context.bot.send_message(chat_id=user_id, text=text)
        await update.message.reply_text("✅ Matn foydalanuvchiga yuborildi.")
    elif 'btn_user' in context.user_data:
        user_id = context.user_data.pop('btn_user')
        try:
            btn_name, btn_text = text.split('|')
            keyboard = [[InlineKeyboardButton(btn_name.strip(), callback_data='custom')]]
            await context.bot.send_message(chat_id=user_id, text=btn_text.strip(), reply_markup=InlineKeyboardMarkup(keyboard))
            await update.message.reply_text("✅ Tugma foydalanuvchiga qo‘shildi.")
        except:
            await update.message.reply_text("❌ Format xato. Iltimos: Tugma nomi | Xabar")

# ==========================
# Bot ishga tushirish
# ==========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

# /start
app.add_handler(CommandHandler("start", start))

# Inline tugmalar (privacy, rules, date, time, cancel)
app.add_handler(CallbackQueryHandler(user_buttons, pattern='^(privacy|rules|select_date|date_|time_|cancel)$'))

# Anketa matnini qabul qilish
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_survey))

# Qiz ismi va belgisi/rassm
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_and_sign))
app.add_handler(MessageHandler(filters.PHOTO, handle_name_and_sign))

# Admin paneli
app.add_handler(CallbackQueryHandler(admin_panel, pattern='^(approve|reject|edit|addbtn)_'))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text_input))

print("Bot ishlamoqda...")
app.run_polling()
