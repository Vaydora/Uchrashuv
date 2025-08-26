from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date, timedelta

busy_dates = ["2025-08-27", "2025-08-29"]  # Misol uchun band kunlar

def rules_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Qoidalarni qabul qilaman", callback_data='select_date')]])

def time_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🕗 20:00 - 21:00", callback_data='time_20')],
        [InlineKeyboardButton("🕘 21:00 - 22:00", callback_data='time_21')]
    ])

def available_dates_keyboard():
    today = date.today()
    keyboard = []
    for i in range(7):
        day = today + timedelta(days=i)
        day_str = str(day)
        if day_str in busy_dates:
            keyboard.append([InlineKeyboardButton(f"{day} ❌ Band", callback_data='busy')])
        else:
            keyboard.append([InlineKeyboardButton(f"{day} ✅ Tanlash", callback_data=f'date_{day_str}')])
    return InlineKeyboardMarkup(keyboard)
