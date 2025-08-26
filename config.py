import os

# Bot tokeni va admin ID
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

# Band kunlar
busy_dates = ["2025-08-27", "2025-08-29"]  # YYYY-MM-DD

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
