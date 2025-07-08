import logging
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from aiohttp import web
import pandas as pd
import os

TOKEN = "7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA"
CHAT_ID = "214241911"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 Shatin Racing Bot 已啟動！")

async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "output/3t_report.xlsx"
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            await update.message.reply_document(document=InputFile(f), filename="3T_分析報表.xlsx")
    else:
        await update.message.reply_text("❌ 未搵到報表檔案 output/3t_report.xlsx")

async def handle_request(request):
    return web.Response(text="OK")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", get3t))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://shatin-vps-deploy.onrender.com"
    )

if __name__ == "__main__":
    main()
