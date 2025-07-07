import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))
REPORT_PATH = "output/3t_report.xlsx"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我係沙田賽馬 AI 助理！輸入 /get3t 即可獲取今日報表。")

async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TELEGRAM_USER_ID:
        await update.message.reply_text("你未被授權使用呢個功能。")
        return
    if not os.path.exists(REPORT_PATH):
        await update.message.reply_text("未有報表可供下載。請稍後再試。")
        return
    with open(REPORT_PATH, "rb") as file:
        await update.message.reply_document(document=InputFile(file, filename="3T_報表.xlsx"))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", get3t))
    app.run_polling()
