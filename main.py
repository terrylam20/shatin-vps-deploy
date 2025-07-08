import os
import pandas as pd
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# ===== 1. Bot Token 與 Chat ID 設定 =====
TOKEN = '7386971571:AAG9mg98gV-64RSrYqVGwP46EPo1cF1XWYA'
CHAT_ID = 214241911  # 你的 Telegram 用戶 ID

# ===== 2. 建立 output 資料夾與測試報表 =====
os.makedirs("output", exist_ok=True)
report_path = "output/3t_report.xlsx"

if not os.path.exists(report_path):
    df = pd.DataFrame({
        "馬匹": ["1號馬", "2號馬", "3號馬"],
        "勝出率": [0.2, 0.3, 0.5],
        "值搏率": [1.5, 1.2, 2.1]
    })
    df.to_excel(report_path, index=False)

# ===== 3. 指令處理器：/get3t =====
async def get3t(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(report_path, "rb") as file:
            await update.message.reply_document(
                document=file,
                filename="3t_report.xlsx",
                caption="📊 三T 投注策略報表已送出"
            )
    except Exception as e:
        await update.message.reply_text(f"❌ 報表發送失敗：{e}")

# ===== 4. 啟動 Webhook 應用 =====
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("get3t", get3t))

    # Webhook 模式用 RENDER_EXTERNAL_HOSTNAME
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
