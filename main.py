import os
import pandas as pd
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# ✅ 載入環境變數
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # https://xxx.onrender.com/webhook

# ✅ 建立測試報表
def generate_test_report():
    os.makedirs("output", exist_ok=True)
    file_path = os.path.join("output", "3t_report.xlsx")
    if not os.path.exists(file_path):
        df = pd.DataFrame({
            "馬號": [1, 2, 3],
            "馬名": ["精彩飛動", "雷神之威", "天行健"],
            "賠率": [5.0, 12.0, 3.2],
            "值搏率": [1.25, 2.15, 0.98]
        })
        df.to_excel(file_path, index=False)
        print("✅ 測試報表已建立")
    else:
        print("📄 已存在報表")

# ✅ 傳送報表指令
async def send_3t_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = os.path.join("output", "3t_report.xlsx")
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=f,
                filename="3T_Report.xlsx",
                caption="📊 以下係最新三T報表"
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ 搵唔到報表：output/3t_report.xlsx"
        )

# ✅ 註冊 Webhook
async def setup_webhook(app):
    bot = Bot(token=TOKEN)
    await bot.set_webhook(url=WEBHOOK_URL)
    print(f"🌐 Webhook 已設定：{WEBHOOK_URL}")

# ✅ 主程式
def main():
    print("🚀 啟動中...")
    generate_test_report()

    app = ApplicationBuilder().token(TOKEN).post_init(setup_webhook).build()
    app.add_handler(CommandHandler("get3t", send_3t_excel))
    print("📩 指令 /get3t 已註冊")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_path="/webhook"  # ✅ 對應 Telegram webhook endpoint
    )

if __name__ == "__main__":
    main()
