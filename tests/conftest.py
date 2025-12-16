import pytest
import os
from dotenv import load_dotenv
import mysql.connector as mysql
from pathlib import Path

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

    # Set default values for test environment
    os.environ.setdefault('DB_HOST', os.getenv('DB_HOST', 'localhost'))
    os.environ.setdefault('DB_USERNAME', os.getenv('DB_USERNAME', 'root'))
    os.environ.setdefault('DB_PASSWORD', os.getenv('DB_PASSWORD', ''))
    os.environ.setdefault('DB_NAME', os.getenv('DB_NAME', 'ssisdb_test'))
    os.environ.setdefault('SECRET_KEY', os.getenv('SECRET_KEY', 'test_secret_key'))

    # Initialize test database
    try:
        # Connect without database first
        conn = mysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD')
        )
        cursor = conn.cursor()

        # Initialize database
        sql = load_sql_file('init_test_db.sql')
        # Replace hardcoded database name with configured one
        db_name = os.getenv('DB_NAME', 'ssisdb_test')
        sql = sql.replace('ssisdb_test', db_name)
        
        for statement in sql.split(';'):
            if statement.strip():
                cursor.execute(statement + ';')
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not initialize test database: {e}")


@pytest.fixture(scope='session')
def database_config():
    """Provide MySQL config for test environment"""
    return {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
