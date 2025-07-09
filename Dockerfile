# worker/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 複製 requirements.txt 並安裝套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案進來
COPY .. .

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info", "--hostname=ettoday@%h"]


#此 Dockerfile 會：
#安裝依賴
#複製整個專案進 container
#自動執行 Celery worker（並可被 Flower 監控）