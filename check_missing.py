import pandas as pd
all_urls = pd.read_csv("all_threads_urls_first_crawl.csv", header=None)[0].tolist()
df = pd.read_csv("make_investment_easy_threads_main_posts.csv")
done_urls = set(df['url'])
missing_urls = [u for u in all_urls if u not in done_urls]
print("還沒完成抓取的貼文數：", len(missing_urls))
pd.Series(missing_urls).to_csv("need_to_crawl_remain.csv", index=False)
