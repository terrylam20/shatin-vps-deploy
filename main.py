import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# ⬇️ 載入 .env 變數（可選）
load_dotenv()

# ✅ Token、Chat ID、Webhook URL
TOKEN = "7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA"
CHAT_ID = 214241911
WEBHOOK_URL = "https://shatin-vps-deploy.onrender.com"

# 📦 傳送 3T Excel 檔案
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

# ✅ 主函式：Webhook 模式
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # 加入指令處理器
    app.add_handler(CommandHandler("get3t", send_3t_excel))

    # 設定 webhook 並啟動服務
    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ 錯誤：{e}")
