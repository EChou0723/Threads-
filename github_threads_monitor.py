cd ~/threads_monitor

# 1. 主程式檔案
cat > github_threads_monitor.py << 'EOF'
import os
import time
import random
import re
import requests
import json
from datetime import datetime

# 從環境變數讀取設定
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(msg):
    """發送 Telegram 通知"""
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Telegram 設定缺失")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": msg}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print(f"✅ Telegram 發送成功")
            return True
        else:
            print(f"❌ Telegram 發送失敗，狀態碼: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Telegram 發送例外: {e}")
        return False

def get_threads_posts():
    """獲取 Threads 貼文"""
    try:
        url = "https://www.threads.net/@make_investment_easy"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        # 提取貼文連結
        post_links = re.findall(r'href="/@make_investment_easy/post/([A-Za-z0-9_-]+)"', response.text)
        
        if post_links:
            # 去重並限制數量
            unique_links = list(dict.fromkeys(post_links))[:5]  
            urls = [f"https://www.threads.net/@make_investment_easy/post/{link}" for link in unique_links]
            # 跳過第一個（可能是置頂）
            return urls[1:] if len(urls) > 1 else urls
        else:
            return []
            
    except Exception as e:
        print(f"❌ 獲取貼文失敗: {e}")
        return []

def load_processed_posts():
    """載入已處理的貼文記錄"""
    try:
        if os.path.exists('processed_posts.json'):
            with open('processed_posts.json', 'r') as f:
                return set(json.load(f))
    except:
        pass
    return set()

def save_processed_posts(posts):
    """儲存已處理的貼文記錄"""
    try:
        with open('processed_posts.json', 'w') as f:
            json.dump(list(posts), f)
        print(f"💾 已儲存 {len(posts)} 篇處理記錄")
    except Exception as e:
        print(f"❌ 儲存記錄失敗: {e}")

def get_post_preview(url):
    """獲取貼文預覽內容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # 簡單提取一些可能的內容關鍵字
        content_keywords = re.findall(r'(投資|股票|美股|ETF|基金|理財|財經)', response.text)
        if content_keywords:
            return f"包含: {', '.join(list(dict.fromkeys(content_keywords))[:3])}"
        else:
            return "投資相關貼文"
    except:
        return "新貼文"

def github_monitor():
    """GitHub Actions 監控主函數"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕐 {current_time} - 開始 GitHub Actions 監控")
    
    # 載入已處理的貼文
    processed_posts = load_processed_posts()
    print(f"📚 已處理貼文: {len(processed_posts)} 篇")
    
    # 獲取最新貼文
    latest_urls = get_threads_posts()
    print(f"📱 找到 {len(latest_urls)} 個最新網址")
    
    if not latest_urls:
        send_telegram("⚠️ GitHub 監控: 無法獲取貼文網址")
        return
    
    # 篩選新貼文
    new_urls = [url for url in latest_urls if url not in processed_posts]
    print(f"🆕 發現新貼文: {len(new_urls)} 篇")
    
    success_count = 0
    
    if new_urls:
        for url in new_urls:
            print(f"🔔 處理新貼文: {url}")
            
            # 獲取貼文預覽
            preview = get_post_preview(url)
            
            # 發送通知
            msg = f"🔔 白話投資新貼文！\n\n"
            msg += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            msg += f"📝 {preview}\n"
            msg += f"📱 網址: {url}\n\n"
            msg += f"🤖 來自 GitHub Actions 雲端監控"
            
            if send_telegram(msg):
                success_count += 1
                processed_posts.add(url)
            
            time.sleep(2)  # 避免發送太快
        
        # 儲存記錄
        save_processed_posts(processed_posts)
    
    # 發送總結報告
    summary = f"📊 GitHub Actions 監控完成\n"
    summary += f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    summary += f"🔍 檢查了 {len(latest_urls)} 篇貼文\n"
    summary += f"🆕 發現 {len(new_urls)} 篇新貜文\n"
    summary += f"✅ 成功通知 {success_count} 篇\n\n"
    summary += f"🤖 雲端監控運行正常"
    
    send_telegram(summary)
    print(f"🎉 GitHub Actions 監控完成！")

if __name__ == "__main__":
    github_monitor()
EOF

# 2. GitHub Actions 工作流程
mkdir -p .github/workflows
cat > .github/workflows/monitor.yml << 'EOF'
name: Threads Monitor

on:
  schedule:
    # 每天 UTC 07:00 執行 (台灣時間 15:00)
    - cron: '0 7 * * *'
  workflow_dispatch: # 允許手動觸發

jobs:
  monitor:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
        
    - name: Run monitor
      env:
        BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
        CHAT_ID: ${{ secrets.CHAT_ID }}
      run: python github_threads_monitor.py
      
    - name: Commit processed posts
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add processed_posts.json || true
        git commit -m "Update processed posts [$(date)]" || true
        git push || true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
EOF

# 3. README 說明檔
cat > README.md << 'EOF'
# 白話投資 Threads 監控系統

🤖 自動監控白話投資 Threads 貼文的 GitHub Actions 雲端系統

## ✨ 功能特色
- 📅 每天台灣時間下午 3:00 自動執行
- 🔍 智能跳過置頂貼文，只檢查最新內容
- 📱 檢測到新貼文立即發送 Telegram 通知
- ☁️ 完全雲端運行，不依賴本地電腦
- 💰 完全免費使用 GitHub Actions
- 📊 每日執行總結報告

## 🔔 通知內容
- 新貼文即時通知（包含預覽和連結）
- 每日監控完成報告
- 系統運行狀態

## ⚙️ 已設定
- ✅ Telegram Bot Token
- ✅ Chat ID  
- ✅ 每日自動執行排程
- ✅ 智能內容檢測

## 🚀 系統狀態
系統運行正常，每天準時監控！

---
*最後更新: 2025-09-20*
EOF

# 4. 初始化空的處理記錄檔案
echo '[]' > processed_posts.json

echo "✅ 所有檔案已準備完成！"
ls -la
EOF
