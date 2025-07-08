import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://shatin-vps-deploy.onrender.com")

# === 傳送 3T Excel 檔案 ===
async def send_3t_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "output", "3t_report.xlsx")

    if os.path.exists(file_path):
        with open(file_path, "rb") as doc:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=doc,
                filename="3T_Report.xlsx",
                caption="📊 以下係最新三T報表"
            )
            print("✅ 成功傳送報表給 Telegram 使用者。")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ 錯誤：未能找到報表檔案（output/3t_report.xlsx）"
        )
        print("⚠️ 未找到報表檔案，請確認 output/3t_report.xlsx 是否存在。")

# === Webhook 註冊函數 ===
async def setup_webhook(app):
    bot = Bot(token=TOKEN)
    await bot.set_webhook(url=WEBHOOK_URL)
    print(f"🌐 Webhook 已註冊至：{WEBHOOK_URL}")

# === 主程式 ===
def main():
    print("🚀 正在啟動 Telegram Bot...")

    app = ApplicationBuilder().token(TOKEN).post_init(setup_webhook).build()
    app.add_handler(CommandHandler("get3t", send_3t_excel))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
