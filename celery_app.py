from celery import Celery
import os

# 可根據環境變數切換 RabbitMQ host
broker_url = os.environ.get("CELERY_BROKER", "amqp://worker:worker@localhost:5672//")

print("📡 Celery broker is:", broker_url)

app = Celery(
    'ettoday_worker',
    broker=broker_url,
    include=['tasks']
)
