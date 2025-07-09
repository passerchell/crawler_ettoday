# producer.py
import pika
import json

# 要爬的關鍵字清單
keywords = ["50嵐", "CoCo都可", "COMEBUY", "迷客夏", "麻古茶坊", "清心福全", "手搖飲"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='crawl_tasks')

for keyword in keywords:
    message = json.dumps({"keyword": keyword, "max_pages": 3})
    channel.basic_publish(exchange='', routing_key='crawl_tasks', body=message)
    print(f"📤 已送出任務：{keyword}")

connection.close()
