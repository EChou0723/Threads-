from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random, pandas as pd

def extract_post_text(driver, url):
    driver.get(url)
    time.sleep(random.uniform(7, 14))
    # blocks = driver.find_elements(By.XPATH, '//article') # threads 實際DOM名
    blocks = driver.find_elements(By.XPATH, '//div[@role="region"]')
    items = []
    for block in blocks:
        try:
            # 假設裡面span為文字內容區
            spans = block.find_elements(By.XPATH, ".//span[@dir='auto']")
            for s in spans:
                txt = s.text.strip()
                if len(txt) > 3:
                    items.append(txt)
        except Exception:
            continue
    if not items:
        print("需要重登入或異常")
        return "LOGIN_REQUIRED"
    return '\n'.join(list(dict.fromkeys(items)))

# 主流程
driver = webdriver.Chrome()
driver.get("https://www.threads.com/")
input("請在(自動開啟的)視窗完成登入，進入自己的頁面，再到 Terminal 按 Enter ...")
urls = pd.read_csv('你的網址list.csv')['url'].tolist()
results = []
for i, url in enumerate(urls):
    print(f"{i+1}/{len(urls)} 訪問: {url}")
    post_text = extract_post_text(driver, url)
    results.append({"url": url, "post_text": post_text})
    time.sleep(random.uniform(7, 14))
driver.quit()
pd.DataFrame(results).to_csv("補抓內容.csv", index=False)
