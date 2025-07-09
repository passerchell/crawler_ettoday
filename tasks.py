from celery_app import app
from et_crawler import crawl_ettoday
from db import insert_article

@app.task(name="tasks.crawl_and_store")
def crawl_and_store(keyword, max_pages=3):
    print(f"🛍 [Celery] 收到任務：{keyword}，頁數：{max_pages}")
    articles = crawl_ettoday(keyword, max_pages)
    for article in articles:
        insert_article(article)
        print(f"✅ 已寫入：{article['title'][:30]}...")
    print(f"🎉 完成任務：{keyword}，共 {len(articles)} 則")