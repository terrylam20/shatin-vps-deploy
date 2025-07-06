import logging
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ 設定環境變數
TOKEN = os.getenv("TELEGRAM_TOKEN")
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_USER_ID", "0"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-service-name.onrender.com/webhook

# ✅ Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("未經授權。")
        return
    await update.message.reply_text("你好，我係沙田賽馬 AI 助理！輸入 /get3t 即可獲取今日報表。")

# ✅ /get3t 指令
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("未經授權。")
        return

    filepath = "output/3t_report.xlsx"
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            await update.message.reply_document(document=InputFile(f, filename="3t_report.xlsx"))
    else:
        await update.message.reply_text("報表暫未準備好，請稍後再試。")

# ✅ 主程式入口（Webhook 模式）
if __name__ == "__main__":
    if not TOKEN or not WEBHOOK_URL:
        print("❌ TOKEN 或 WEBHOOK_URL 未設定")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", send_excel))

    # ✅ 啟動 Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )