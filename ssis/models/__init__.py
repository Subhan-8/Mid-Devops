import mysql.connector as mysql
from os import getenv

import time

# Lazily initialized DB connection for better testability
db = None
cursor = None

def init_connection():
    global db, cursor
    if db is None or cursor is None:
        retries = 30
        while retries > 0:
            try:
                host = getenv('DB_HOST', 'db')
                print(f"Connecting to database at {host}...")
                db = mysql.connect(
                    host=host,
                    user=getenv('DB_USER', 'root'),
                    password=getenv('DB_PASSWORD', '123SubhanS'),
                    database=getenv('DB_NAME', 'ssisdb')
                )
                cursor = db.cursor()
                print("Database connected successfully")
                break
            except mysql.Error as err:
                print(f"Database connection failed: {err}")
                retries -= 1
                if retries == 0:
                    print("Max retries reached. Exiting.")
                    raise err
                print(f"Retrying in 2 seconds... ({retries} retries left)")
                time.sleep(2)
