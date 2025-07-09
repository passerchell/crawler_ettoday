from celery_app import app

if __name__ == "__main__":
    keyword = "手搖飲"  # 設定要爬蟲的關鍵字
    max_pages = 2 # 設定要爬蟲的頁數, 0 代表不限制頁數

    print(f"📤 發送任務中：關鍵字 = {keyword}, 頁數 = {max_pages}")
    try:
        result = app.send_task("tasks.crawl_and_store", args=[keyword, max_pages])
        print(f"✅ 任務已送出，任務 ID：{result.id}")
    except Exception as e:
        print(f"❌ 任務發送失敗：{e}")
