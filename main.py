import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ✅ Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8443))

# ✅ 定義 /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤖 AI 馬匹報表系統已啟動！你可以試用 /get3t 或 /testreport")

# ✅ 模擬 /get3t 指令（真實情況請改成實際報表回傳）
async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        await update.message.reply_document(document=open(file_path, "rb"))
    else:
        await update.message.reply_text("❌ 搵唔到報表檔案：output/3t_report.xlsx")

# ✅ 測試報表指令
async def testreport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📊 測試報表已生成（模擬中），實際功能待接駁分析模組")

# ✅ 主程式
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", get3t))
    app.add_handler(CommandHandler("testreport", testreport))

    # ✅ 正確使用 webhook_url
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
