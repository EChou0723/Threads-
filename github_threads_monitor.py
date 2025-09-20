import os
import time
import requests
import json
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Telegram 設定缺失")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": msg}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram 發送成功")
            return True
        else:
            print(f"❌ Telegram 發送失敗，狀態碼: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Telegram 發送例外: {e}")
        return False

def load_processed_posts():
    try:
        if os.path.exists('processed_posts.json'):
            with open('processed_posts.json', 'r') as f:
                return set(json.load(f))
    except:
        pass
    return set()

def save_processed_posts(posts):
    try:
        posts_list = list(posts)[-50:]
        with open('processed_posts.json', 'w') as f:
            json.dump(posts_list, f)
        print(f"💾 已儲存 {len(posts_list)} 篇處理記錄")
    except Exception as e:
        print(f"❌ 儲存記錄失敗: {e}")

def github_monitor():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕐 {current_time} - 開始 GitHub Actions 監控")
    
    # 發送測試訊息
    test_msg = f"🤖 GitHub Actions 測試成功！\n\n"
    test_msg += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    test_msg += f"✅ 系統運行正常\n"
    test_msg += f"🔔 明天下午3:00開始正式監控白話投資！"
    
    if send_telegram(test_msg):
        print("🎉 測試成功！")
    else:
        print("❌ 測試失敗")

if __name__ == "__main__":
    github_monitor()
