import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ Telegram Bot Token（直接寫入）
TOKEN = "7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA"

# ✅ Webhook 相關設定
PORT = int(os.environ.get("PORT", 8443))
WEBHOOK_URL = f"https://shatin-vps-deploy.onrender.com"

# ✅ 指令處理：傳送 3T 報表
async def send_3t_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(file_path, "rb"),
            filename="3T_報表.xlsx",
            caption="📊 以下係最新三T報表"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ 搵唔到報表！請先產生 `output/3t_report.xlsx`"
        )

# ✅ 主程序（async webhook）
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # ➕ 加入指令 handler
    app.add_handler(CommandHandler("get3t", send_3t_excel))

    # ✅ 初始化 + 啟動 Webhook
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Bot 已透過 Webhook 成功啟動")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
