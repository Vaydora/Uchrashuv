# main.py
from handlers import start, accept_rules, select_date, select_time, handle_survey, save_obraz, admin_panel, admin_text_input
from keyboards import rules_keyboard, obraz_keyboard, available_dates_keyboard, time_keyboard
from config import ADMIN_ID, busy_dates, questions
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

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
