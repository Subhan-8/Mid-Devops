import pytest
import os
from dotenv import load_dotenv
import mysql.connector as mysql
from pathlib import Path
from werkzeug.security import generate_password_hash

def load_sql_file(filename):
    """Read SQL file content"""
    file_path = Path(__file__).parent / 'data' / filename
    with open(file_path, 'r') as f:
        return f.read()

def pytest_configure(config):
    """Load environment variables and initialize test database"""
    # Load environment variables
    if os.path.exists('.env.test'):
        load_dotenv('.env.test')
    elif os.path.exists('.env'):
        load_dotenv('.env')

    # Force test values for environment to avoid leaking prod .env
    os.environ['DB_HOST'] = os.getenv('DB_HOST') or '127.0.0.1'
    os.environ['DB_USERNAME'] = os.getenv('DB_USERNAME') or 'root'
    os.environ['DB_PASSWORD'] = os.getenv('DB_PASSWORD') or ''
    os.environ['DB_NAME'] = 'ssisdb_test'
    os.environ['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'test_secret_key'

    # Initialize test database
    try:
        # Connect without database first
        conn = mysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD')
        )
        cursor = conn.cursor()

        # Drop the test database if it exists
        cursor.execute(f"DROP DATABASE IF EXISTS {os.getenv('DB_NAME')}")
        conn.commit()
        
        # Initialize database in steps
        cursor.execute("DROP DATABASE IF EXISTS ssisdb_test")
        cursor.execute("CREATE DATABASE ssisdb_test")
        cursor.execute("USE ssisdb_test")
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS college (
                code VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                photo_url VARCHAR(255)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course (
                code VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                collegecode VARCHAR(10),
                FOREIGN KEY (collegecode) REFERENCES college(code)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id VARCHAR(20) PRIMARY KEY,
                firstname VARCHAR(50) NOT NULL,
                middlename VARCHAR(50),
                lastname VARCHAR(50) NOT NULL,
                coursecode VARCHAR(10),
                collegecode VARCHAR(10),
                year INT,
                gender VARCHAR(10),
                photo VARCHAR(255),
                FOREIGN KEY (coursecode) REFERENCES course(code),
                FOREIGN KEY (collegecode) REFERENCES college(code)
            )
        """)
        
        # Insert test data
        # Insert test admin with a real password hash for 'test_password'
        test_hash = generate_password_hash('test_password')
        cursor.execute(
            "INSERT IGNORE INTO admin (username, password) VALUES (%s, %s)",
            ('test_admin', test_hash)
        )
        
        cursor.execute("""
            INSERT IGNORE INTO college (code, name) 
            VALUES ('COL1', 'Test College')
        """)
        
        cursor.execute("""
            INSERT IGNORE INTO course (code, name, collegecode) 
            VALUES ('CRS1', 'Test Course', 'COL1')
        """)
        
        cursor.execute("""
            INSERT IGNORE INTO students (id, firstname, lastname, coursecode, collegecode, year, gender) 
            VALUES ('2021-0001', 'Test', 'Student', 'CRS1', 'COL1', 1, 'Male')
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not initialize test database: {e}")
        raise  # Re-raise the exception to fail tests if DB setup fails


@pytest.fixture(scope='session')
def database_config():
    """Provide MySQL config for test environment"""
    return {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
