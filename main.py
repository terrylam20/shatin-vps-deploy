
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
REPORT_PATH = "output/3t_report.xlsx"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我係沙田賽馬 AI 助理！輸入 /get3t 即可獲取今日報表。")

async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(REPORT_PATH):
        await update.message.reply_document(document=open(REPORT_PATH, "rb"))
    else:
        await update.message.reply_text("未找到報表檔案，請稍後再試。")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", get3t))
    app.run_polling()
