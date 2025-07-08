import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ChatAction
import pandas as pd

# ✅ Telegram Token 與 Chat ID
TOKEN = "7386971571:AAF3fY1vIRgBMnGxcEOBlAAca_q5HWr5iLY"
CHAT_ID = 214241911

# ✅ 報表檔案路徑
OUTPUT_FOLDER = "output"
REPORT_FILENAME = "3t_report.xlsx"
REPORT_PATH = os.path.join(OUTPUT_FOLDER, REPORT_FILENAME)

# ✅ 日誌設定
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ✅ 確保 output 資料夾存在
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ✅ 建立示範 Excel 報表（如未存在）
if not os.path.isfile(REPORT_PATH):
    df = pd.DataFrame({
        "馬匹": ["馬王", "冷腳", "爆冷王"],
        "值搏率": [1.5, 2.1, 3.8],
        "建議下注": ["主腳", "拖腳", "拖腳"]
    })
    df.to_excel(REPORT_PATH, index=False)

# ✅ 處理 /start 指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 歡迎使用 Shatin Racing Bot！輸入 /get3t 可獲取今日三T報表。")

# ✅ 處理 /get3t 指令：傳送 Excel
async def get_3t_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.chat.send_action(action=ChatAction.UPLOAD_DOCUMENT)
        await update.message.reply_document(document=open(REPORT_PATH, "rb"))
    except Exception as e:
        await update.message.reply_text(f"❌ 發生錯誤：{str(e)}")

# ✅ 主程序：建立應用程式
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get3t", get_3t_report))

    # ✅ 設定 Webhook（Render 會自動處理 URL，無需 hardcode）
    app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=URL + TOKEN,
    secret_token=TOKEN
)
