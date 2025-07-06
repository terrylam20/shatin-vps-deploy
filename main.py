import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ Token 同用戶 ID（臨時寫死，方便你 debug）
TOKEN = "7386971571:AAExoA9q7RhREOzR_edIbBLAyhRRZg-9BsA"
ALLOWED_USER_ID = 214241911

# ✅ Logging 設定
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("未經授權。")
        return
    await update.message.reply_text("你好，我係沙田賽馬 AI 助理！輸入 /get3t 即可獲取今日報表。")

# ✅ /get3t 指令
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("未經授權。")
        return

    filepath = "output/3t_report.xlsx"
    try:
        with open(filepath, "rb") as f:
            await update.message.reply_document(document=InputFile(f, filename="3t_report.xlsx"))
    except FileNotFoundError:
        await update.message.reply_text("報表暫未準備好，請稍後再試。")

# ✅ 主程式
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", send_excel))
    app.run_polling()