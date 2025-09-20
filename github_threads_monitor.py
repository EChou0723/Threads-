import os
import requests
from datetime import datetime
import json

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": msg}
        response = requests.get(url, params=params, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def get_threads_posts_alternative():
    """使用替代方法獲取貼文"""
    try:
        # 方法1: 嘗試不同的 User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        url = "https://www.threads.net/@make_investment_easy"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # 更寬鬆的模式匹配
            import re
            patterns = [
                r'/post/([A-Za-z0-9_-]+)',
                r'threads\.net/@make_investment_easy/post/([A-Za-z0-9_-]+)',
                r'"post_id":"([A-Za-z0-9_-]+)"',
            ]
            
            all_links = []
            for pattern in patterns:
                matches = re.findall(pattern, response.text)
                all_links.extend(matches)
            
            if all_links:
                unique_links = list(dict.fromkeys(all_links))[:5]
                urls = [f"https://www.threads.net/@make_investment_easy/post/{link}" for link in unique_links]
                return urls
        
        return []
        
    except Exception as e:
        print(f"獲取貼文失敗: {e}")
        return []

def main():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Starting monitor at {current_time}")
    
    # 讀取處理記錄
    processed_posts = set()
    try:
        with open('processed_posts.json', 'r') as f:
            processed_posts = set(json.load(f))
    except:
        processed_posts = set()
    
    # 嘗試獲取貼文
    latest_urls = get_threads_posts_alternative()
    
    if latest_urls:
        print(f"找到 {len(latest_urls)} 個貼文網址")
        
        # 篩選新貼文
        new_urls = [url for url in latest_urls if url not in processed_posts]
        
        if new_urls:
            msg = f"🔔 發現 {len(new_urls)} 篇新貼文！\n\n"
            for i, url in enumerate(new_urls[:3], 1):  # 最多顯示3篇
                msg += f"{i}. {url}\n"
            
            msg += f"\n📅 {current_time}\n🤖 GitHub Actions 監控"
            
            send_telegram(msg)
            
            # 添加到處理記錄
            processed_posts.update(new_urls)
        else:
            msg = f"📊 監控完成 - 沒有新貼文\n📅 {current_time}"
            send_telegram(msg)
    else:
        # 即使無法獲取貼文，也發送狀態報告
        msg = f"⚠️ 監控狀態報告\n\n"
        msg += f"📅 {current_time}\n"
        msg += f"📝 已處理 {len(processed_posts)} 篇貼文\n"
        msg += f"🔄 系統運行正常，但無法獲取新貼文\n"
        msg += f"💡 可能原因：Threads 反爬蟲機制\n\n"
        msg += f"🤖 GitHub Actions 持續監控中..."
        
        send_telegram(msg)
    
    # 儲存記錄
    try:
        with open('processed_posts.json', 'w') as f:
            json.dump(list(processed_posts), f)
    except Exception as e:
        print(f"Save error: {e}")

if __name__ == "__main__":
    main()
