import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="12345",
        database="amazon_scraper",
        cursorclass=pymysql.cursors.DictCursor
        )