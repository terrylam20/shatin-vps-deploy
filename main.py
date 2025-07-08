import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ 你嘅 Token + Chat ID
TOKEN = "7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA"
CHAT_ID = 214241911

# ✅ Webhook URL（Render HTTPS 連結）
WEBHOOK_URL = "https://shatin-vps-deploy.onrender.com"

# 📦 指令：/get3t 傳送 Excel 檔案
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, "rb"))
        await context.bot.send_message(chat_id=update.effective_chat.id, text="📊 已發送最新三T報表！")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ 找不到報表檔案！請先產生 3T Excel。")

# ✅ 主函式（async + webhook 模式）
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("get3t", send_excel))

    # 必須 initialize 再 start（Webhook 模式）
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=WEBHOOK_URL)
    await app.updater.start_polling()  # 有需要可關掉 polling

    print("✅ Bot 已啟動 webhook，等緊指令！")

    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
