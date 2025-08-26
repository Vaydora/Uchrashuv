from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers import start, accept_privacy, accept_rules, select_date, select_time, handle_survey, save_obraz, admin_panel
from config import BOT_TOKEN

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(accept_privacy, pattern='^privacy$'))
app.add_handler(CallbackQueryHandler(accept_rules, pattern='^rules$'))
app.add_handler(CallbackQueryHandler(select_date, pattern='^select_date$'))
app.add_handler(CallbackQueryHandler(select_time, pattern='^time_'))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_survey))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_obraz))
app.add_handler(MessageHandler(filters.PHOTO, save_obraz))
app.add_handler(CallbackQueryHandler(admin_panel, pattern='^(approve|reject)_'))

print("Bot ishlamoqda...")
app.run_polling()
