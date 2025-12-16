import mysql.connector as mysql
from os import getenv

import time

# Lazily initialized DB connection for better testability
db = None
cursor = None

def init_connection():
    global db, cursor
    if db is None or cursor is None:
        retries = 5
        while retries > 0:
            try:
                db = mysql.connect(
                    host=getenv('DB_HOST', 'db'),
                    user=getenv('DB_USER', 'root'),
                    password=getenv('DB_PASSWORD', '123$ubhanS'),
                    database=getenv('DB_NAME', 'ssisdb')
                )
                cursor = db.cursor()
                print("Database connected successfully")
                break
            except mysql.Error as err:
                print(f"Database connection failed: {err}")
                retries -= 1
                if retries == 0:
                    raise err
                print(f"Retrying in 5 seconds... ({retries} retries left)")
                time.sleep(5)
