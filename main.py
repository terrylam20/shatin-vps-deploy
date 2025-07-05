
import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import filetype

# Token & User ID
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = 214241911

# Logging 設定
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    await update.message.reply_text("你好，我係沙田賽馬智能助理！你可以輸入 /我要3treport 以獲取最新分析報表。")

# /我要3treport 指令
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            await update.message.reply_document(document=InputFile(f))
    else:
        await update.message.reply_text("⚠️ 暫時搵唔到報表，請稍後再試。")

# 主函數 - 啟動 Webhook
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("我要3treport", send_excel))

    webhook_url = "https://shatin-vps-deploy.onrender.com/webhook"
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8888)),
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
