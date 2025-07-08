import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from aiohttp import web

# === Logging 設定 ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === 讀取環境變數 ===
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
PORT = int(os.environ.get("PORT", 8443))

# === /start 指令 ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🎉 你好！請輸入 /get3t 獲取三T報表 Excel 文件！")

# === /get3t 指令 ===
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # 自動建立 output 資料夾（避免錯誤）
        os.makedirs("output", exist_ok=True)

        file_path = 'output/3t_report.xlsx'
        if not os.path.isfile(file_path):
            await update.message.reply_text("❌ 找不到報表：output/3t_report.xlsx")
            return

        with open(file_path, 'rb') as f:
            await update.message.reply_document(
                document=InputFile(f, filename="3T報表.xlsx"),
                caption="📊 三T報表已送達，祝你好運！🍀"
            )

    except Exception as e:
        logging.error(f"發送 Excel 發生錯誤: {e}")
        await update.message.reply_text(f"⚠️ 發生錯誤：{e}")

# === 主程序 ===
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", send_excel))

    # Webhook 伺服器啟動
    async def handler(request):
        data = await request.json()
        update = Update.de_json(data, app.bot)
        await app.process_update(update)
        return web.Response()

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
