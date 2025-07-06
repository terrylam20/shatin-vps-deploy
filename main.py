
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# 設定 Token 同用戶 ID
TOKEN = "7386971571:AAExoA9q7RhREOzR_edIbBLAyhRRZg-9BsA"
ALLOWED_USER_ID = 214241911  # 你個 Telegram user ID

# 設定 logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 指令 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("未經授權。")
        return
    await update.message.reply_text("你好，我係沙田賽馬 AI 助理！可以輸入 /我要3T報表")

# 指令 /我要3T報表
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("未經授權。")
        return

    filepath = "output/3t_report.xlsx"
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            await update.message.reply_document(document=InputFile(f, filename="3t_report.xlsx"))
    else:
        await update.message.reply_text("報表未準備好。")

# 主程式入口
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("我要3T報表", send_excel))
    app.run_polling()
