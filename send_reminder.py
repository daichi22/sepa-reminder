# send_reminder.py
import os
import requests

LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
GROUP_ID = os.environ.get('_GROUP_ID')

headers = {
    'Authorization': f'Bearer {LINE_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

data = {
    "to": LINE_GROUP_ID,
    "messages": [
        {
            "type": "text",
            "text": "鍵とネット誰ですか？"
        }
    ]
}

response = requests.post(
    'https://api.line.me/v2/bot/message/push',
    headers=headers,
    json=data
)

if response.status_code == 200:
    print("✅ メッセージ送信成功")
else:
    print(f"❌ 送信失敗: {response.status_code} - {response.text}")
