from telegram import Update, BotCommand, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7309821581:AAHodQcZRGFlAYbPPbkd6_NBgEzqZr--Yi4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Dasturchaga kirish", web_app={"url": "https://abdurahmonjon.github.io/test-attendance-mini-app/frontend/mainpage.html"})]
    ]
    await update.message.reply_text(
        "Mini App`ni ochish uchun pastdagi tugmachani bosing",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

def main():
    print("Starting the bot...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
    print("Bot is running...")

if __name__ == '__main__':
    main()
