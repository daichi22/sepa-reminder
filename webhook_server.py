from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os
import sys


# あなたのLINEチャネルの情報を入れてください
LINE_CHANNEL_ACCESS_TOKEN = 'VTXwqgGo1yGnweP/nf9aEDaFXQQAss/WDSeA2zKgx88C25vNPbWbaYfs3QuaOgRwVxd4VAVyfBSMr2vePNcF0b87ajdIVwMpkRaDkN339dzKjnjo6Ptu24AvslCV2nmquK7Ii01yEfeCBIhG7tEQWwdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '911ccf8f35ea5bc6512e3846098ba5cb'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

# Webhookエンドポイント
@app.route("/callback", methods=['POST'])
def callback():
    # LINEからの署名を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    print("💡 リクエストボディ:", body)

    # 署名チェックしてイベント処理
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# メッセージ受信時の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("📌 受信したソースタイプ:", event.source.type)
    sys.stdout.flush()

    if event.source.type == 'group':
        print("📌 グループID:", event.source.group_id)
    elif event.source.type == 'room':
        print("📌 ルームID:", event.source.room_id)
    elif event.source.type == 'user':
        print("📌 ユーザーID:", event.source.user_id)

    # 応答（何か返してくれるように）
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="うけとりました！")
    )

    print(f"[DEBUG] group_id: {event.source.group_id}")
    print(f"[DEBUG] user_id: {event.source.user_id}")
    print(f"[DEBUG] message: {event.message.text}")



if __name__ == "__main__":
    app.run(port=5000)
