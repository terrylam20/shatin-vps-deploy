import os
import logging
from telegram import Update, InputFile
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)

# ✅ 指令回覆：/start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Shatin Racing Bot 已啟動！")

# ✅ 指令回覆：/get3t 傳送 Excel
async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        await update.message.reply_document(document=InputFile(file_path))
    else:
        await update.message.reply_text("❌ 暫時搵唔到報表喎（output/3t_report.xlsx）")

# ✅ 主函式：Webhook 啟動邏輯
async def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get3t", get3t))

    # 🔁 先 initialize 再啟動 webhook（解決錯誤）
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    await application.updater.start_polling()  # Safe fallback
    await application.run_until_disconnected()

# ✅ 執行入口
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
