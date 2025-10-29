import pytest
from ssis import create_app
import mysql.connector as mysql
import os

@pytest.fixture(scope='session')
def db_connection(database_config):
    """Create a test database connection"""
    connection = mysql.connect(**database_config)
    yield connection
    connection.close()


@pytest.fixture()
def app(db_connection):
    """
    Create Flask app with test DB injected.
    Each test gets isolated transactions via rollback.
    """
    app = create_app()
    app.config.update({
        'TESTING': True,
        'DB_CONNECTION': db_connection,
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_USERNAME': os.getenv('DB_USERNAME'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_NAME': os.getenv('DB_NAME'),
        'SECRET_KEY': os.getenv('SECRET_KEY')
    })

    # Start a transaction
    cursor = db_connection.cursor()
    cursor.execute("START TRANSACTION")

    yield app

    # Rollback DB changes after each test
    cursor.execute("ROLLBACK")
    cursor.close()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data or b"SSIS" in response.data


def test_admin_login_page(client):
    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b"Login" in response.data or b"Admin" in response.data
