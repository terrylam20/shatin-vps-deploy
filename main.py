import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yaml

# 載入 config.yaml
def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
TOKEN = config["token"]
USER_ID = config["user_id"]

# 傳送 3t_report.xlsx 給指定 user_id
async def send_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        await update.message.reply_text("❌ 你無權使用此指令")
        return
    try:
        await update.message.reply_document(document=open("output/3t_report.xlsx", "rb"))
        await update.message.reply_text("✅ 已傳送報表")
    except Exception as e:
        await update.message.reply_text(f"發生錯誤：{e}")

# 設定主程式
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("get3t", send_excel))
    print("✅ Telegram Bot 已啟動，等待指令中...")
    app.run_polling()
