# handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_ID, BUSY_DATES
from keyboards import rules_keyboard, obraz_keyboard, available_dates_keyboard, time_keyboard
from datetime import date, timedelta

# Foydalanuvchi ma'lumotlari
user_data = {}
orders = {}  # admin ko‘rishi uchun barcha foydalanuvchi ma’lumotlari

# Anketa savollari
questions = [
    "👤 Kimni kutyapsiz?",
    "✍️ Ism:",
    "💼 Kasb:",
    "🎯 Uchrashuv maqsadi:",
    "💬 Suhbat mavzulari:",
    "📍 Manzil:",
    "🎭 Obraz:"
]

# -------------------------------
# /start komandasi
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 *Salom! Men Bob, sizning shaxsiy uchrashuv maslahatchingiz.*\n\n"
        "📅 Uchrashuv buyurtmasini berish uchun davom eting.",
        reply_markup=rules_keyboard(),
        parse_mode='Markdown'
    )

# -------------------------------
# Qoidalarni qabul qilish
# -------------------------------
async def accept_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_data[user_id] = {"rules_accepted": True, "survey": {}, "q_index": 0}

    await query.edit_message_text("✅ Qoidalar qabul qilindi!\n\nIsmingizni kiriting:")

# -------------------------------
# Ism va anketani qabul qilish
# -------------------------------
async def handle_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data or not user_data[user_id].get("rules_accepted"):
        await update.message.reply_text("❌ Avval qoidalarni qabul qiling! /start bosing.")
        return

    if "ask_name" in user_data[user_id]:
        # Qiz ismi
        user_data[user_id]["girl_name"] = update.message.text
        user_data[user_id].pop("ask_name")
        user_data[user_id]["ask_sign"] = True
        await update.message.reply_text("🔖 Tanib olish uchun belgini yozing yoki rasm jo‘nating:")
        return

    if "ask_sign" in user_data[user_id]:
        # Belgisi yoki rasm
        if update.message.photo:
            user_data[user_id]["sign"] = "Rasm yuborildi"
        else:
            user_data[user_id]["sign"] = update.message.text
        user_data[user_id].pop("ask_sign")
        orders[user_id] = user_data[user_id]  # admin uchun saqlash

        # Adminga xabar yuborish
        msg = "📝 Yangi buyurtma va anketa:\n"
        for i, answer in enumerate(user_data[user_id]["survey"].values()):
            msg += f"{questions[i]} {answer}\n"
        msg += f"👧 Qiz ismi: {user_data[user_id]['girl_name']}\n"
        msg += f"🔖 Tanib olish belgisi / rasm: {user_data[user_id]['sign']}\n"
        msg += f"📅 Uchrashuv kuni: {user_data[user_id].get('selected_date')}\n"
        msg += f"⏰ Vaqti: {user_data[user_id].get('selected_time')}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

        await update.message.reply_text("✅ Anketa to‘ldirildi va adminga yuborildi.")
        return

    # Oddiy anketa savollari
    q_index = user_data[user_id]["q_index"]
    user_data[user_id]["survey"][q_index] = update.message.text
    q_index += 1
    if q_index < len(questions):
        user_data[user_id]["q_index"] = q_index
        await update.message.reply_text(questions[q_index])
    else:
        user_data[user_id]["q_index"] = None
        user_data[user_id]["ask_name"] = True
        await update.message.reply_text("👧 Iltimos, qizning ismini kiriting:")

# -------------------------------
# Obrazni tanlash
# -------------------------------
async def save_obraz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "obraz_aqlli_boy":
        user_data[user_id]["obraz"] = "Aqlli boy bola"
    elif query.data == "obraz_oddiy":
        user_data[user_id]["obraz"] = "Oddiy bola"
    elif query.data == "obraz_kuldiradigan":
        user_data[user_id]["obraz"] = "Kuldiradigan bola"
    await query.edit_message_text(f"✅ Obraz saqlandi: {user_data[user_id]['obraz']}")

# -------------------------------
# Sanalarni tanlash
# -------------------------------
def get_available_dates():
    today = date.today()
    dates = []
    for i in range(7):
        day = today + timedelta(days=i)
        dates.append(str(day))
    return dates

async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    dates = get_available_dates()
    await query.message.reply_text("📅 Bo'sh kunlardan birini tanlang:", reply_markup=available_dates_keyboard(dates))

async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    selected_date = query.data.split('_')[1]
    user_data[user_id]["selected_date"] = selected_date
    await query.message.reply_text(f"⏰ {selected_date} uchun vaqtni tanlang:", reply_markup=time_keyboard())

# -------------------------------
# Admin paneli
# -------------------------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = int(data.split('_')[1])

    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("❌ Siz admin emassiz!")
        return

    if data.startswith('approve_'):
        await context.bot.send_message(chat_id=user_id, text="✅ Buyurtmangiz tasdiqlandi!")
        await query.edit_message_text("Buyurtma tasdiqlandi.")
    elif data.startswith('reject_'):
        await context.bot.send_message(chat_id=user_id, text="❌ Buyurtmangiz rad etildi.")
        await query.edit_message_text("Buyurtma rad etildi.")
    elif data.startswith('edit_'):
        await query.edit_message_text("Admin: Foydalanuvchiga yuboriladigan matnni yozing.")
        context.user_data['edit_user'] = user_id
    elif data.startswith('addbtn_'):
        await query.edit_message_text("Admin: Yangi tugma nomi va matnini yozing (Tugma nomi | Xabar).")
        context.user_data['btn_user'] = user_id
    elif data.startswith('adddate_'):
        new_date = data.split('_')[1]
        if new_date not in BUSY_DATES:
            BUSY_DATES.append(new_date)
            await query.edit_message_text(f"✅ {new_date} bo‘sh kunlar ro‘yxatiga qo‘shildi.")
    elif data.startswith('vieworders'):
        if not orders:
            await query.edit_message_text("📂 Hozircha buyurtmalar mavjud emas.")
        else:
            msg = "📝 Buyurtmalar ro‘yxati:\n\n"
            for uid, info in orders.items():
                msg += f"👤 Foydalanuvchi ID: {uid}\n"
                for k, v in info.items():
                    msg += f"{k}: {v}\n"
                msg += "\n"
            await query.edit_message_text(msg)