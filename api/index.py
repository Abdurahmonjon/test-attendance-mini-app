from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request
import os
import threading
import time
import requests

# Environment variables for configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7309821581:AAHodQcZRGFlAYbPPbkd6_NBgEzqZr--Yi4")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://test-attendance-mini-app.vercel.app/")  # Vercel will provide this during deployment
RENDER_URL = os.getenv("RENDER_URL", "https://file-receiver-bot.onrender.com/")

# Flask app for Vercel
app = Flask(__name__)

# Telegram bot setup
tg_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Start command triggered!")
    keyboard = [
        [InlineKeyboardButton("Dasturchaga kirish", web_app={"url": "https://abdurahmonjon.github.io/test-attendance-mini-app/frontend/mainpage.html"})]
    ]
    await update.message.reply_text(
        "Mini App`ni ochish uchun pastdagi tugmachani bosing",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# Add Telegram handlers
tg_app.add_handler(CommandHandler("start", start))

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        print("Received data:", data)
        tg_app.update_queue.put(Update.de_json(data, tg_app.bot))
        return "OK", 200
    return "Hello, I am your Telegram bot!", 200

# Set the webhook URL during initialization
@app.before_first_request
def set_webhook():
    if WEBHOOK_URL:
        tg_app.bot.set_webhook(WEBHOOK_URL)

# Function to keep the Render app awake
def ping_render():
    while True:
        try:
            print(f"Pinging Render app at {RENDER_URL}...")
            response = requests.get(RENDER_URL)
            print(f"Render app response: {response.status_code}")
        except Exception as e:
            print(f"Error pinging Render app: {e}")
        time.sleep(600)  # Ping every 10 minutes

# Start the cron job in a separate thread
def start_cron_job():
    thread = threading.Thread(target=ping_render, daemon=True)
    thread.start()

if __name__ == "__main__":
    start_cron_job()  # Start the cron job
    app.run(debug=True)
