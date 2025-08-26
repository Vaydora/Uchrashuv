from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from handlers import start, accept_rules, select_date, select_time, handle_survey, save_obraz, admin_panel

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Commandlar
app.add_handler(CommandHandler("start", start))

# CallbackQuery
app.add_handler(CallbackQueryHandler(accept_rules, pattern='rules'))
app.add_handler(CallbackQueryHandler(select_date, pattern='select_date'))
app.add_handler(CallbackQueryHandler(select_time, pattern='time_'))

# Foydalanuvchi xabarlarini olish
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_survey))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, save_obraz))

# Admin panel
app.add_handler(CallbackQueryHandler(admin_panel, pattern='admin_'))

print("Bot ishga tushdi...")
app.run_polling()
