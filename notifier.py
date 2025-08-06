# notifier.py
import requests
from datetime import datetime

# 自分のDiscordのWebhook URLを設定
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/YOUR/DISCORD/URL'

def send_discord_notify(message: str):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{now_str}] {message}"
    
    data = {
        "content": message
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"[エラー] 通知失敗：{response.status_code} - {response.text}")
    else:
        print("[成功] 通知を送信しました")
