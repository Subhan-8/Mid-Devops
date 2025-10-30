import mysql.connector as mysql
from os import getenv

# Lazily initialized DB connection for better testability
db = None
cursor = None

def init_connection():
    global db, cursor
    if db is None or cursor is None:
        db = mysql.connect(
            host=getenv('DB_HOST', 'db'),
            user=getenv('DB_USER', 'root'),
            password=getenv('DB_PASSWORD', '123$ubhanS'),
            database=getenv('DB_NAME', 'ssisdb')
        )
        cursor = db.cursor()
