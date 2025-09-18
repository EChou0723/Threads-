# Threads Content Scraper 🕸️

一個用於抓取 Threads 社群平台內容的 Python 爬蟲工具，專門設計用來收集和分析投資相關貼文內容。

## ✨ 專案特色

- 🔐 **智能登入檢測** - 自動偵測登入狀態並提示手動登入
- 🛡️ **防反爬機制** - 隨機延時、User-Agent 偽裝、分批休息
- 🔄 **自動補抓系統** - 智能檢測異常內容並生成補抓清單
- 📊 **品質控制** - 自動去重、異常檢測、成功率統計
- 🤖 **NotebookLM 整合** - 直接輸出適合 AI 分析的格式

## 📊 專案成果

- **總抓取量**: 447 篇貼文
- **成功率**: 87.7%
- **有效內容**: 383 篇
- **總字數**: 33 萬字
- **平均長度**: 1,609 字元/篇

## 🚀 快速開始
pip install -r requirements.txt

### 環境需求
pip install -r requirements.txt

### 基本使用
python src/threads_batch_spider.py

### 步驟說明

1. 程式會自動開啟 Chrome 瀏覽器
2. 手動登入 Threads 帳號
3. 確認登入成功後按 Enter
4. 程式自動開始抓取內容
5. 完成後輸出 CSV 檔案

## 📁 檔案說明

### 核心腳本
- `threads_batch_spider.py` - 完整版爬蟲（推薦使用）
- `threads_post_content_crawler.py` - 簡化版爬蟲

### 資料檔案
- `all_threads_urls_first_crawl.csv` - 所有貼文網址清單
- `make_investment_easy_threads_main_posts.csv` - 原始抓取結果
- `make_investment_easy_threads_main_posts_clean.csv` - 清理後的資料
- `threads_for_notebooklm.csv` - NotebookLM 專用格式
- `threads_urls_to_refetch.csv` - 需要補抓的網址清單

### 輸出格式
- `Bai-Hua-Tou-Zi-ThreadsNei-Rong.txt` - 純文字格式，適合 AI 分析

## 🔧 核心功能

### 1. 智能登入檢測
if "登入" in driver.page_source or "Login" in driver.page_source:
print(f"[ERROR] 需重新登入: {url}")
return "LOGIN_REQUIRED"

### 2. 防反爬機制
time.sleep(random.uniform(10, 18)) # 隨機延時
if (idx + 1) % 20 == 0:
time.sleep(120) # 每20篇休息2分鐘


### 3. 自動補抓系統
def detect_empty_posts(input_csv, output_csv):
error_conditions = ["", "LOGIN_REQUIRED", "NO_TEXT_FOUND", "nan"]
empty_urls = df[df["post_text_and_replies"].isin(error_conditions)]
empty_urls.to_csv(output_csv)


## 📈 品質控制

### 成功率統計
- ✅ 有效內容: 392 篇 (87.7%)
- ❌ 空白內容: 48 篇
- ❌ 登入失效: 7 篇

### 內容品質
- 平均長度: 1,609 字元
- 最長內容: 6,853 字元
- 重複內容: < 2%

## 🤖 NotebookLM 整合

處理後的資料可直接上傳至 Google NotebookLM：

1. 使用 `threads_for_notebooklm.csv` 或 `Bai-Hua-Tou-Zi-ThreadsNei-Rong.txt`
2. 上傳至 NotebookLM 建立知識庫
3. 享受 AI 問答功能

範例問題：
- "白話投資對技術分析的觀點是什麼？"
- "整理所有關於選擇權的討論"
- "分析風險管理的核心要點"

## ⚠️ 常見問題

### 空白 CSV 問題
**原因**: 未在 Selenium 開啟的瀏覽器內登入
**解決**: 等待提示後在自動開啟的瀏覽器視窗內手動登入

### HTTP 500 錯誤
**原因**: 觸發反爬機制或 IP 被暫時封鎖
**解決**: 增加延時間隔或更換網路環境

### 內容重複
**原因**: Threads 分享機制或頁面結構異常
**解決**: 使用內建的去重功能

詳細疑難排解請參考 [troubleshooting.md](docs/troubleshooting.md)

## 🛠️ 客製化設定

### 修改目標帳號
username = "your_target_account"
profile_url = "https://www.threads.com/@your_target_account"


### 調整延時設定
time.sleep(random.uniform(5, 10)) # 減少延時
time.sleep(random.uniform(15, 25)) # 增加延時


## 📊 資料分析建議

1. **內容分析**: 使用 NLP 技術分析主題分布
2. **情感分析**: 追蹤市場情緒變化
3. **時間序列**: 分析觀點演變趨勢
4. **知識圖譜**: 建立概念關聯網路

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 發起 Pull Request

## 📄 授權條款

MIT License - 詳見 [LICENSE](LICENSE) 檔案

## 🙏 致謝

- [Selenium](https://selenium-python.readthedocs.io/) - Web 自動化框架
- [Pandas](https://pandas.pydata.org/) - 資料處理工具
- [白話投資](https://www.threads.com/@make_investment_easy) - 內容來源

## 📞 聯繫資訊

如有問題或建議，歡迎聯繫：
- GitHub Issues: [專案 Issues 頁面]
- Email: [你的信箱]

---

⭐ 如果這個專案對你有幫助，請給個星星支持！

📋 requirements.txt
selenium>=4.15.0
pandas>=2.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0

🚫 .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Browser drivers
chromedriver*
geckodriver*

# Large data files (optional)
data/raw/*.csv
data/processed/*.csv
*.txt

# Logs
*.log

# Credentials (if any)
.env
credentials.json

🔧 docs/troubleshooting.md
# 疑難排解指南

## 常見問題與解決方案

### 1. 空白 CSV 檔案

#### 問題描述
程式執行完成，但 CSV 檔案中只有網址，內容欄位全部空白。

#### 根本原因
- Selenium 開啟的是全新瀏覽器 session
- 與本機已登入的瀏覽器完全隔離
- 程式以「未登入」狀態訪問頁面

#### 解決方案
1. 等待程式提示「請先登入...」
2. 在**自動開啟的瀏覽器視窗**內手動登入 Threads
3. 確認能看到個人主頁後按 Enter
4. 不要在本機其他瀏覽器視窗登入

### 2. HTTP 500 錯誤

#### 問題描述
抓取過程中出現 `HTTP ERROR 500` 或被導向錯誤頁面。

#### 可能原因
- 請求頻率過高觸發反爬機制
- IP 被暫時封鎖
- 網站臨時維護

#### 解決方案
1. 增加延時間隔：`time.sleep(random.uniform(15, 30))`
2. 更換網路環境（手機熱點）
3. 稍後再試（通常 1-2 小時後自動解除）

### 3. 內容重複問題

#### 問題描述
不同網址抓到相同的貼文內容。

#### 可能原因
- Threads 分享/轉發機制
- 頁面結構動態變化
- 選擇器抓取錯誤區域

#### 解決方案
使用內建去重功能：
df_clean = df.drop_duplicates(subset=['post_text_and_replies'], keep='first')

### 4. Chrome Driver 問題

#### 問題描述
`selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH`

#### 解決方案
1. 安裝 Chrome 瀏覽器
2. 下載對應版本的 ChromeDriver
3. 將 ChromeDriver 放入 PATH 或專案目錄
4. 或使用 webdriver-manager 自動管理：
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

### 5. 記憶體不足

#### 問題描述
處理大量資料時記憶體不足或程式崩潰。

#### 解決方案
1. 分批處理：
batch_size = 50
for i in range(0, len(url_list), batch_size):
batch = url_list[i:i+batch_size]
# 處理批次

2. 及時釋放記憶體：
df = None # 釋放大型 DataFrame
gc.collect() # 強制垃圾回收

### 6. 編碼問題

#### 問題描述
CSV 檔案中文顯示亂碼。

#### 解決方案
使用正確的編碼格式：
df.to_csv('output.csv', encoding='utf-8-sig', index=False)

## 偵錯技巧

### 1. 啟用詳細日誌
import logging
logging.basicConfig(level=logging.DEBUG)

### 2. 保存錯誤頁面
if "error" in driver.page_source:
driver.save_screenshot("error_page.png")
with open("error_page.html", "w") as f:
f.write(driver.page_source)
### 3. 逐步偵錯
print(f"當前網址: {driver.current_url}")
print(f"頁面標題: {driver.title}")
print(f"找到區塊數: {len(blocks)}")
## 效能優化

### 1. 減少不必要的元素載入
options.add_argument("--disable-images")
options.add_argument("--disable-css")
### 2. 使用無頭模式（測試用）
options.add_argument("--headless")
### 3. 設定頁面載入策略
options.add_argument("--page-load-strategy=eager")
📁 最終檔案清單
必要檔案：
README.md - 專案說明

requirements.txt - 相依套件

.gitignore - 忽略檔案清單

src/threads_batch_spider.py - 主要爬蟲腳本

docs/troubleshooting.md - 疑難排解

範例資料檔案（可選）：
data/raw/all_threads_urls_first_crawl.csv - 網址清單範例

data/processed/threads_for_notebooklm.csv - 處理後資料範例
