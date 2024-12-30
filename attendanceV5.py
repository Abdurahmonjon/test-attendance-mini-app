import os
import requests
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
import time

# Constants
TOKEN = '7309821581:AAHodQcZRGFlAYbPPbkd6_NBgEzqZr--Yi4'
RENDER_URL = 'https://test-attendance-mini-app.onrender.com'

# Create a Flask app to keep the service alive and bind to a port
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot is running"

# Function to ping the Render app
def ping_render():
    while True:
        try:
            print(f"Pinging Render app at {RENDER_URL}...")
            response = requests.get(RENDER_URL)
            print(f"Render app response: {response.status_code}")
        except Exception as e:
            print(f"Error pinging Render app: {e}")
        time.sleep(600)  # Ping every 10 minutes

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Dasturchaga kirish", web_app={"url": "https://abdurahmonjon.github.io/test-attendance-mini-app/frontend/mainpage.html"})]
    ]
    await update.message.reply_text(
        "Mini App`ni ochish uchun pastdagi tugmachani bosing",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Function to run the Telegram bot
def run_telegram_bot():
    try:
        application = ApplicationBuilder().token(TOKEN).build()
        print(f"Telegram bot started")
        application.add_handler(CommandHandler("start", start))

        # Start the bot
        print("Bot is starting...")
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"Error in run_telegram_bot: {e}")

# Function to run Flask
def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Main function
def main():
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start the cron job to ping the Render app in a separate thread
    cron_thread = threading.Thread(target=ping_render, daemon=True)
    cron_thread.start()

    # Run the Telegram bot in the main thread
    run_telegram_bot()

if __name__ == "__main__":
    main()
