# 🧃 crawler_ettoday-worker

ETtoday 新聞平台飲料品牌關鍵字爬蟲｜Celery 分散式爬蟲架構 + Docker 化部署

---

## 📌 專案簡介

本專案為一套可擴充的分散式爬蟲系統，專門用於爬取 ETtoday 新聞網站中與「飲料品牌」相關的文章資料（例如：50嵐、CoCo 都可、清心福全、迷客夏等），並儲存至 MySQL 資料庫。

設計目標為方便團隊後續透過 Docker Hub 團隊協作、雲端部署與可擴充的 worker 架構。

---

## 🧩 架構組成

| 元件            | 說明                                       |
|------------------|--------------------------------------------|
| `Celery`         | 任務佇列與非同步爬蟲任務管理                |
| `RabbitMQ`       | 任務傳遞中介者（broker）                    |
| `Flower`         | Web UI 管理 Celery 任務與 worker 狀態       |
| `MySQL`          | 儲存爬取下來的新聞資料                      |
| `Docker Compose` | 多容器協作與建構部署                        |
| `requests + BS4` | 網頁爬取核心函式庫                          |

---

## 📦 功能特點

- ✅ 可指定關鍵字與頁數，爬取 ETtoday 搜尋結果
- ✅ 自動擷取標題、日期、內文與網址
- ✅ 分散式架構支援多台 worker 同時執行任務
- ✅ Celery + Flower 管理任務狀態與錯誤追蹤
- ✅ Docker Image 可用於本機測試或雲端部署

---

## 🚀 使用方式
docker run chingp/crawler_ettoday-worker:0.0.1

##發送任務
使用 Python send_task.py 發送爬蟲任務：

python
from celery_app import app
**app.send_task("tasks.crawl_and_store", args=["50嵐", 2])**
