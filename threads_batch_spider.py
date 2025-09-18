import requests
import os
import time
import random
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Telegram 設定，已由助理代入你的資訊
BOT_TOKEN = '輸入你的 Token '
CHAT_ID = '輸入你的 CHAY_ID'
def send_telegram(msg):
    """發送訊息到 Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": msg}
    requests.get(url, params=params)
def extract_post_and_replies(driver, url, username):
    """從 Threads 貼文抓取主要內容與留言，返回字串"""
    driver.get(url)
    time.sleep(random.uniform(8, 15))  # 隨機等待防反爬
    items = []
    try:
        if "登入" in driver.page_source or "Login" in driver.page_source:
            print(f"[ERROR] 需重新登入: {url}")
            return "LOGIN_REQUIRED"
        blocks = driver.find_elements(By.XPATH, '//div[@role="region"]') or driver.find_elements(By.XPATH, '//article')
        print(f"解析貼文區塊數: {len(blocks)} in {url}")
        for block in blocks:
            try:
                spans = block.find_elements(By.XPATH, ".//span[@dir='auto']")
                for s in spans:
                    txt = s.text.strip()
                    if re.search(r'[。！？，,.A-Za-z0-9]', txt) and len(txt) > 3:
                        items.append(txt)
            except Exception:
                continue
        if len(items) == 0:
            print(f"[WARN] 沒抓到主文/留言: {url}")
            return "NO_TEXT_FOUND"
    except Exception as e:
        print(f"[ERROR] Parse error: {e} url: {url}")
        return f"FETCH_ERROR: {e}"
    return '\n'.join(list(dict.fromkeys(items)))
def detect_empty_posts(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    error_conditions = ["", "LOGIN_REQUIRED", "NO_TEXT_FOUND", "nan"]
    urls = df[df["post_text_and_replies"].astype(str).str.strip().isin(error_conditions)]["url"].tolist()
    if urls:
        pd.Series(urls).to_csv(output_csv, index=False)
        print(f"需補抓網址共 {len(urls)} 筆，已輸出 {output_csv}")
    else:
        print("所有內容都已正常抓取完成！")
    return len(urls)
if __name__ == "__main__":
    # 請將下方路徑修改成你實際 iCloud 桌面的資料夾路徑
    base_dir = "/Users/yourbaby/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Python 爬 Threads 資料"
    
    finished_file = os.path.join(base_dir, "make_investment_easy_threads_main_posts.csv")
    refetch_file = os.path.join(base_dir, "threads_urls_to_refetch.csv")
    all_url_file = os.path.join(base_dir, "all_threads_urls_first_crawl.csv")
    
    username = "make_investment_easy"
    
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    options.add_argument("accept-language=zh-TW,zh;q=0.9,en;q=0.8")
    
    if os.path.exists(finished_file):
        empty_count = detect_empty_posts(finished_file, refetch_file)
        if empty_count > 0:
            url_list = pd.read_csv(refetch_file).iloc[:, 0].tolist()
            print(f"【本次優先補抓 {len(url_list)} 篇】")
        else:
            print("【沒有需要補抓的內容，將進行全量檢查】")
            url_list = pd.read_csv(all_url_file).iloc[:, 0].tolist()
    else:
        url_list = pd.read_csv(all_url_file).iloc[:, 0].tolist()
        print(f"【首次抓取，共 {len(url_list)} 篇】")
    
    already_done = set()
    if os.path.exists(finished_file):
        try:
            df_exist = pd.read_csv(finished_file)
            normal_posts = df_exist[~df_exist["post_text_and_replies"].astype(str).str.strip().isin(["LOGIN_REQUIRED", "NO_TEXT_FOUND", "", "nan"])]
            already_done.update(normal_posts["url"].tolist())
        except Exception as e:
            print(f"讀取歷史記錄失敗: {e}")
    
    pending_list = [u for u in url_list if u not in already_done]
    print(f"待抓取共：{len(pending_list)} 篇")
    
    if len(pending_list) == 0:
        print("所有內容都已完成抓取！")
        send_telegram("🎉 所有內容都已成功抓取完成！")
        exit()
    
    driver = webdriver.Chrome(options=options)
    results = []
    try:
        driver.get("https://www.threads.com/")
        input("請在自動開啟的瀏覽器內完成登入 Threads，確認能看到個人主頁後按 Enter ...")
    
        for idx, url in enumerate(pending_list):
            print(f"[{idx+1}/{len(pending_list)}] 抓取: {url}")
            try:
                post_text = extract_post_and_replies(driver, url, username)
                results.append({"url": url, "post_text_and_replies": post_text})
                if "LOGIN_REQUIRED" in post_text:
                    print("檢測到登入失效，請重新登入...")
                    input("請在瀏覽器重新登入後按 Enter 繼續...")
            except Exception as e:
                print(f"[ERROR] {url}: {e}")
                results.append({"url": url, "post_text_and_replies": f"FETCH_ERROR: {e}"})
            wait_time = random.uniform(10, 18)
            print(f"等待 {wait_time:.1f} 秒...")
            time.sleep(wait_time)
            if (idx + 1) % 20 == 0:
                print("已抓 20 篇，休息 2 分鐘...")
                time.sleep(120)
    finally:
        driver.quit()
    
    df_new = pd.DataFrame(results)
    if os.path.exists(finished_file):
        try:
            df_exist = pd.read_csv(finished_file)
            df_exist_clean = df_exist[~df_exist["url"].isin([r["url"] for r in results])]
            df_final = pd.concat([df_exist_clean, df_new]).drop_duplicates("url", keep="last")
        except Exception as e:
            print(f"合併失敗: {e}")
            df_final = df_new
    else:
        df_final = df_new
    df_final.to_csv(finished_file, index=False, encoding="utf-8-sig")
    print(f"\n完成！共處理 {len(results)} 篇，已存檔至 {finished_file}")
    
    final_empty = detect_empty_posts(finished_file, refetch_file)
    
    new_posts_count = len([r for r in results if r["url"] not in already_done])
    has_crawl_error = any("FETCH_ERROR" in str(r["post_text_and_replies"]) for r in results)
    has_login_error = any("LOGIN_REQUIRED" in str(r["post_text_and_replies"]) for r in results)
    has_other_error = final_empty > 0
    
    if new_posts_count > 0:
        for r in results:
            if r["url"] not in already_done:
                msg = f"白話投資有新貼文！\n網址：{r['url']}\n內容：{r['post_text_and_replies'][:300]}..."
                send_telegram(msg)
        print(f"白話投資有新貼文：{new_posts_count} 篇！")
    if has_crawl_error:
        msg = "⚠️ 爬蟲執行過程發生抓取錯誤，請檢查 log！"
        send_telegram(msg)
        print(msg)
    if has_login_error:
        msg = "⚠️ 登入失效需手動補登，請檢查主控台！"
        send_telegram(msg)
        print(msg)
    if has_other_error:
        msg = f"⚠️ 尚有 {final_empty} 篇內容需補抓（請查看 refetch 清單）！"
        send_telegram(msg)
        print(msg)
    if final_empty == 0 and not has_crawl_error and not has_login_error:
        send_telegram("🎉 所有內容都已成功抓取完成！")
    print("\n【本次執行完畢】")
