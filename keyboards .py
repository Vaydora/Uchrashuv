from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date, timedelta
from config import busy_dates

# Maxfiylik shartnomasi tugmalari
privacy_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("✅ Roziman", callback_data='rules')]
])

# Uchrashuv qoidalari tugmalari
rules_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("✅ Qoidalarni qabul qilaman", callback_data='select_date')]
])

# Vaqt tanlash tugmalari
time_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("🕗 20:00 - 21:00", callback_data='time_20')],
    [InlineKeyboardButton("🕘 21:00 - 22:00", callback_data='time_21')]
])

# Sanalarni chiqarish
def available_dates_keyboard():
    today = date.today()
    buttons = []
    for i in range(7):
        day = today + timedelta(days=i)
        if str(day) in busy_dates:
            buttons.append([InlineKeyboardButton(f"{day} ❌ Band", callback_data='busy')])
        else:
            buttons.append([InlineKeyboardButton(f"{day} ✅ Tanlash", callback_data=f'date_{day}')])
    return InlineKeyboardMarkup(buttons)
