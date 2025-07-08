import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode
import pathlib
from aiohttp import web
import asyncio

TOKEN = os.environ.get("BOT_TOKEN", "7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA")
CHAT_ID = os.environ.get("CHAT_ID", "214241911")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://shatin-vps-deploy.onrender.com/webhook")

logging.basicConfig(level=logging.INFO)

async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = 'output/3t_report.xlsx'
    if not os.path.exists(file_path):
        await update.message.reply_text("❌ 報表未產生，請稍後再試")
        return
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'),
                                    filename='3T報表.xlsx',
                                    caption="📊 這是你要的 3T 分析報表")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 歡迎使用 Shatin Racing Bot！輸入 /get3t 可獲取今日報表")

async def webhook_handler(request):
    data = await request.json()
    await application.update_queue.put(Update.de_json(data, application.bot))
    return web.Response()

async def main():
    global application
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get3t", get3t))

    await application.bot.set_webhook(WEBHOOK_URL)

    app = web.Application()
    app.router.add_post("/webhook", webhook_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    logging.info(f"✅ Webhook is running on port {port}")
    await application.start()
    await application.updater.start_polling()
    await application.wait_closed()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
