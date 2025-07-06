import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot 已啟動")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/", methods=["GET"])
def home():
    return "Shatin Race Bot is running."

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK"

if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path="",
        webhook_url=os.getenv("WEBHOOK_URL")
    )