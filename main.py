import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "your-bot-token")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app-name.onrender.com")

async def send_3t_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        with open(file_path, "rb") as doc:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=doc,
                filename="3T_Report.xlsx",
                caption="📊 以下係最新三T報表"
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ 搵唔到報表檔案：output/3t_report.xlsx"
        )

async def setup_webhook(app):
    bot = Bot(token=TOKEN)
    await bot.set_webhook(url=WEBHOOK_URL)

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(setup_webhook).build()
    app.add_handler(CommandHandler("get3t", send_3t_excel))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL  # ✅ 只可以用 webhook_url，唔可以用 webhook_path
    )

if __name__ == "__main__":
    main()
