import pymysql

# 連線設定
connection = pymysql.connect(
    host="mysql",
    user="root",
    password="test",
    database="news_db",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

def insert_article(article):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO news_articles (keyword, title, url, date, content)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            article['keyword'],
            article['title'],
            article['url'],
            article['date'],
            article['content']
        ))
    connection.commit()
