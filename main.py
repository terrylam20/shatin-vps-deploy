import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "your-bot-token")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app-name.onrender.com/webhook")

async def send_excel_report(update: Update, context: ContextTypes.DEFAULT_TYPE, file_path: str, caption: str):
    if os.path.exists(file_path):
        with open(file_path, "rb") as doc:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=doc,
                filename=os.path.basename(file_path),
                caption=caption
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"❌ 搵唔到報表檔案：{file_path}"
        )

async def send_3t_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_excel_report(update, context, "output/3t_report.xlsx", "📊 以下係最新三T報表")

async def send_hv_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_excel_report(update, context, "output/investment_report_HV_2025-07-10.xlsx", "📈 以下係快活谷投資報表")

async def send_st_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_excel_report(update, context, "output/investment_report_ST_2025-07-13.xlsx", "📈 以下係沙田投資報表")

async def send_3t_hv_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_excel_report(update, context, "output/3t_report_HV_2025-07-10.xlsx", "📊 以下係快活谷三T報表")

async def send_3t_st_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_excel_report(update, context, "output/3t_report_ST_2025-07-13.xlsx", "📊 以下係沙田三T報表")

async def setup_webhook(app):
    bot = Bot(token=TOKEN)
    await bot.set_webhook(url=WEBHOOK_URL)

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(setup_webhook).build()

    app.add_handler(CommandHandler("get3t", send_3t_excel))
    app.add_handler(CommandHandler("gethv", send_hv_excel))
    app.add_handler(CommandHandler("getst", send_st_excel))
    app.add_handler(CommandHandler("get3t_hv", send_3t_hv_excel))
    app.add_handler(CommandHandler("get3t_st", send_3t_st_excel))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL,
        webhook_path="/webhook"  # 加返呢個 path handler
    )

if __name__ == "__main__":
    main()
