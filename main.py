import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_ID = 214241911

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我係沙田賽馬智能助理！")

async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        await update.message.reply_text("未授權用戶。")
        return
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            await update.message.reply_document(document=InputFile(file, filename="3T報表.xlsx"))
    else:
        await update.message.reply_text("未搵到報表。")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("我要3T報表", send_excel))

if __name__ == "__main__":
    app.run_polling()
