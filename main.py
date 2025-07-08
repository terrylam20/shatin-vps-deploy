import os
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# ⬇️ 載入 .env 變數（可選）
load_dotenv()

# ✅ 你嘅 Token + Webhook URL（可從環境變數或硬編碼）
TOKEN = os.getenv("BOT_TOKEN", "7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://shatin-vps-deploy.onrender.com")

# 📦 指令處理：傳送 3T 報表
async def send_3t_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        with open(file_path, "rb") as doc:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=doc,
                filename="3T_報表.xlsx",
                caption="📊 以下係最新三T報表"
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ 搵唔到報表檔案：output/3t_report.xlsx"
        )

# ✅ 主函式：註冊 Webhook 並啟動
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("get3t", send_3t_excel))

    # ✅ 第一次部署必需：向 Telegram 註冊 Webhook
    async def setup():
        bot = Bot(token=TOKEN)
        await bot.set_webhook(url=WEBHOOK_URL)
    asyncio.run(setup())

    # ✅ 啟動 Webhook 伺服器
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()