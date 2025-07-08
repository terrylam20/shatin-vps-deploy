import os
import pandas as pd
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# ✅ 載入環境變數
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

# ✅ 啟動時建立測試報表（只做一次）
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
        print("✅ 測試報表已建立：output/3t_report.xlsx")
    else:
        print("ℹ️ 已存在報表：output/3t_report.xlsx")

# ✅ 指令回應邏輯：傳送報表
async def send_3t_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = os.path.join("output", "3t_report.xlsx")
    if os.path.exists(file_path):
        with open(file_path, "rb") as doc:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=doc,
                filename="3T_Report.xlsx",
                caption="📊 以下係最新三T報表（測試）"
            )
            print("✅ 已傳送報表至 Telegram 使用者")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ 搵唔到報表：output/3t_report.xlsx"
        )
        print("⚠️ 報表不存在，請確認 output 資料夾")

# ✅ Webhook 註冊
async def setup_webhook(app):
    bot = Bot(token=TOKEN)
    await bot.set_webhook(url=WEBHOOK_URL)
    print(f"🌐 Webhook 設定完成：{WEBHOOK_URL}")

# ✅ 主啟動函式
def main():
    print("🚀 正在啟動 Telegram Bot...")
    generate_test_report()

    app = ApplicationBuilder().token(TOKEN).post_init(setup_webhook).build()
    app.add_handler(CommandHandler("get3t", send_3t_excel))
    print("🔗 指令 /get3t 已註冊")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        path="/webhook",  # ✅ 加入這行（修正錯誤）
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
