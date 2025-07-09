# worker.py
import pika
import json
from et_crawler import crawl_ettoday
from db import insert_article

def callback(ch, method, properties, body):
    task = json.loads(body)
    keyword = task.get("keyword")
    max_pages = task.get("max_pages", 3)

    print(f"✅ 收到任務：{keyword}（最多 {max_pages} 頁）")
    articles = crawl_ettoday(keyword, max_pages)

    for article in articles:
        insert_article(article)
        print(f"📝 已寫入：{article['title'][:20]}...")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='crawl_tasks')

channel.basic_consume(queue='crawl_tasks', on_message_callback=callback, auto_ack=True)
print('🕓 等待任務中（Ctrl+C 可中止）...')
channel.start_consuming()
