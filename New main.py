from telegram import Bot, Update, InputFile
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes
import logging
import os
import filetype

# 設定 Token 同用戶 ID
TOKEN = "7386971571:AAHk_xIj4dekByYNlHUqhGSWAzCqhLojWpU"
ALLOWED_USER_ID = 214241911  # 你個 Telegram user ID

# 設定 logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 指令回覆
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好，我係沙田賽馬智能助理！你可以輸入觀察、評語或賽馬問題，我會自動分析。")

# 處理文字輸入
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    text = update.message.text
    print(f"收到用戶輸入：{text}")
    await update.message.reply_text(f"✅ 已收到你嘅觀察：「{text}」，AI 模型會即時更新分析結果。")

# 處理圖片輸入
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    photo_file = await update.message.photo[-1].get_file()
    file_path = "/tmp/temp.jpg"
    await photo_file.download_to_drive(file_path)

    kind = filetype.guess(file_path)
    if kind:
        extension = kind.extension
    else:
        extension = "unknown"

    await update.message.reply_text(f"📸 圖片已接收（格式：{extension}），稍後會分析！")

# 主程式
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()
