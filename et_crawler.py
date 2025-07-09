# et_crawler.py
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime  # ✅ 加入 datetime 用來轉換時間格式

# 自訂 headers 避免被網站阻擋
headers = {"User-Agent": "Mozilla/5.0"}

def parse_article(url):
    """解析單篇新聞文章內容"""
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 取得標題
        title = soup.select_one("h1.title")

        # 取得時間標籤並轉換格式（例如：'2025年06月07日 18:53' ➜ '2025-06-07 18:53:00'）
        time_tag = soup.select_one("time.date")
        raw_date = time_tag.text.strip() if time_tag else ""
        try:
            date_obj = datetime.strptime(raw_date, "%Y年%m月%d日 %H:%M")  # ✅ 解析中文日期
            date = date_obj.strftime("%Y-%m-%d %H:%M:%S")  # ✅ 轉換為標準 MySQL DATETIME 格式
        except Exception as e:
            print(f"⚠️ 無法解析日期：{raw_date}，原因：{e}")
            date = None  # 或可用空字串 date = ""

        # 擷取內文段落
        article_body = soup.select("div.story > p")
        content = "\n".join(p.text.strip() for p in article_body if p.text.strip())

        return {
            "title": title.text.strip() if title else "",
            "url": url,
            "date": date,  # ✅ 使用已轉換格式的日期
            "content": content
        }

    except Exception as e:
        print(f"❌ 錯誤擷取: {url}，原因：{e}")
        return None

def crawl_ettoday(keyword, max_pages=3):
    """爬取 ETtoday 搜尋結果，根據關鍵字與最大頁數"""
    results = []
    page = 1

    while True:
        search_url = f"https://www.ettoday.net/news_search/doSearch.php?keywords={keyword}&idx={page}"
        print(f"  📄 抓取第 {page} 頁：{search_url}")
        try:
            res = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = soup.select(".box_2 h2 a")  # 抓取新聞標題連結

            if not articles:
                print(f"  ✅ 沒有更多文章，結束「{keyword}」")
                break

            for a in articles:
                article_url = a['href']
                data = parse_article(article_url)
                if data:
                    data['keyword'] = keyword
                    results.append(data)
                time.sleep(1)  # ✅ 友善爬蟲，避免觸發風控

            page += 1
            if max_pages > 0 and page > max_pages:
                break

        except Exception as e:
            print(f"  ❌ 第 {page} 頁發生錯誤：{e}")
            break

    return results
