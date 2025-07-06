import logging
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ 從環境變數讀取 Token 同 User ID
TOKEN = os.getenv("TELEGRAM_TOKEN")
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_USER_ID", "0"))

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
    await update.message.reply_text("你好，我係沙田賽馬 AI 助理！你可以輸入 /我要3T報表 取得 Excel 文件。")

# ✅ /我要3T報表 指令
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

# ✅ 主程式
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("我要3T報表", send_excel))  # 中文指令
    app.run_polling()