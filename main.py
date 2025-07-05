from telegram import Bot, Update, InputFile
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes
import logging
import os

# Token & 用戶 ID
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
    await update.message.reply_text("你好，我係沙田賽馬智能助手，已準備好為你服務！")

# /get3treport 指令：傳送報表
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        document = InputFile(file_path)
        await update.message.reply_document(document=document)
    else:
        await update.message.reply_text("⚠️ 暫時搵唔到報表，請稍後再試。")

# 主函數 - 啟動 Webhook 伺服器
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3treport", send_excel))

    # 設定 Webhook URL
    webhook_url = "https://shatin-vps-deploy.onrender.com/webhook"
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8888)),
        webhook_url=webhook_url,
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())