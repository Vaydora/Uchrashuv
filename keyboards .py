# keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date, timedelta
from config import BUSY_DATES

# -------------------------------
# Qoidalarni qabul qilish tugmasi
# -------------------------------
def rules_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔒 Qoidalarni o‘qib chiqdim va Roziman ✅", callback_data="accept_rules")]
    ]
    return InlineKeyboardMarkup(keyboard)

# -------------------------------
# Bo‘sh sanalarni chiqarish
# -------------------------------
def available_dates_keyboard(dates):
    keyboard = []
    for d in dates:
        if d in BUSY_DATES:
            keyboard.append([InlineKeyboardButton(f"{d} ❌ Band", callback_data="busy")])
        else:
            keyboard.append([InlineKeyboardButton(f"{d} ✅ Tanlash", callback_data=f"date_{d}")])
    return InlineKeyboardMarkup(keyboard)

# -------------------------------
# Vaqt tanlash
# -------------------------------
def time_keyboard():
    keyboard = [
        [InlineKeyboardButton("🕗 20:00 - 21:00", callback_data="time_20")],
        [InlineKeyboardButton("🕘 21:00 - 22:00", callback_data="time_21")]
    ]
    return InlineKeyboardMarkup(keyboard)

# -------------------------------
# Admin paneli tugmalari (misol)
# -------------------------------
def admin_keyboard(user_id):
    keyboard = [
        [InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{user_id}")],
        [InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}")],
        [InlineKeyboardButton("✏️ Matn tahrir", callback_data=f"edit_{user_id}")],
        [InlineKeyboardButton("➕ Tugma qo‘shish", callback_data=f"addbtn_{user_id}")],
        [InlineKeyboardButton("➕ Bo‘sh kun qo‘shish", callback_data=f"adddate_{date.today()}")],
        [InlineKeyboardButton("📂 Buyurtmalarni ko‘rish", callback_data="vieworders")]
    ]
    return InlineKeyboardMarkup(keyboard)