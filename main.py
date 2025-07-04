
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Token（你新生成的）
TOKEN = "7386971571:AAHk_xIj4dekByYNlHUqhGSWAzCqhlojWpU"

# 簡單 NLP 規則關鍵詞（可日後擴展成模型）
def analyze_text(text):
    response = []
    if "爆汗" in text or "流汗" in text:
        response.append("💦 馬匹疑似體能狀況差")
    if "精神唔集中" in text:
        response.append("⚠️ 注意：馬匹精神狀況可能有問題")
    if "未操好" in text:
        response.append("❌ 馬匹操練未足，風險較高")
    if "肌肉結實" in text or "神情好" in text:
        response.append("✅ 馬匹體態理想，可留意")
    if "爆咗汗" in text and "未操好" in text:
        response.append("🔥 高風險：體能未復，需審慎處理")
    return "\n".join(response) if response else "🤖 暫未有明確判斷，請輸入更多觀察資訊"

# 回覆用戶訊息
def handle_message(update, context):
    user_text = update.message.text
    reply = analyze_text(user_text)
    update.message.reply_text(reply)

# 啟動 bot
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", lambda update, context: update.message.reply_text("👋 歡迎使用 Shatin Racing Bot！請輸入觀察資訊。")))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
