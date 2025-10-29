import pytest
import os
from dotenv import load_dotenv

def pytest_configure(config):
    """Load environment variables before running tests"""

    # Load local test environment
    if os.path.exists('.env.test'):
        load_dotenv('.env.test')

    # Default fallback values
    os.environ.setdefault('DB_HOST', os.getenv('DB_HOST', 'localhost'))
    os.environ.setdefault('DB_USERNAME', os.getenv('DB_USERNAME', 'root'))
    os.environ.setdefault('DB_PASSWORD', os.getenv('DB_PASSWORD', ''))
    os.environ.setdefault('DB_NAME', os.getenv('DB_NAME', 'ssisdb_test'))
    os.environ.setdefault('SECRET_KEY', os.getenv('SECRET_KEY', 'test_secret_key'))


@pytest.fixture(scope='session')
def database_config():
    """Provide MySQL config for test environment"""
    return {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
