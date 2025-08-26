# main.py
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import (
    start,
    accept_rules,
    handle_survey,
    save_obraz,
    admin_panel,
    select_date,
    select_time
)
from keyboards import rules_keyboard, obraz_keyboard, available_dates_keyboard, time_keyboard

def main():
    # Botni ishga tushirish
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Komandalar
    app.add_handler(CommandHandler("start", start))

    # Inline tugmalar
    app.add_handler(CallbackQueryHandler(accept_rules, pattern="^accept_rules$"))
    app.add_handler(CallbackQueryHandler(save_obraz, pattern="^obraz_.*$"))
    app.add_handler(CallbackQueryHandler(admin_panel, pattern="^(approve|reject|edit|addbtn|adddate|vieworders)_.*$"))
    app.add_handler(CallbackQueryHandler(select_date, pattern="^select_date$"))
    app.add_handler(CallbackQueryHandler(select_time, pattern="^date_.*$"))

    # Foydalanuvchi matnlari (anketa, ism, belgilar)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_survey))
    app.add_handler(MessageHandler(filters.PHOTO, handle_survey))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
