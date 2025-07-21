import os
import time
import schedule
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import TextSendMessage

# .envファイルの読み込み
load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

# LINE BotのAPIクライアント
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 🔁 送信関数
def send_reminder():
    print("🔔 リマインド送信中...")
    message = TextSendMessage(text="鍵とネット誰ですか？")
    try:
        line_bot_api.push_message(GROUP_ID, message)
        print("✅ メッセージ送信成功")
    except Exception as e:
        print("❌ メッセージ送信失敗:", e)

# 🗓️ スケジュール設定（火・土・日 21:00）
for day in ['tuesday', 'saturday', 'sunday']:
    schedule.every().day.at("21:00").do(
        lambda d=day: send_reminder() if schedule.datetime.datetime.today().strftime('%A').lower() == d else None
    )

print("🟢 リマインダーBot 起動中...（Ctrl+Cで停止）")

# ⏰ メインループ
while True:
    schedule.run_pending()
    time.sleep(1)
