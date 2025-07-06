import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我係沙田賽馬 AI 助理！輸入 /get3t 即可獲取今日報表。")

async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        await update.message.reply_document(document=open(file_path, "rb"), filename="3T報表.xlsx")
    else:
        await update.message.reply_text("未找到報表，請稍後再試，或確認是否已產生 Excel。")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", get3t))
    app.run_polling()
    