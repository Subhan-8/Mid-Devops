import pytest
from ssis import create_app
from ssis.models.admin import Admin
import os
import mysql.connector as mysql

@pytest.fixture(scope='session')
def db_connection(database_config):
    """Create a test database connection"""
    connection = mysql.connect(**database_config)
    yield connection
    connection.close()

@pytest.fixture
def app(db_connection):
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
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_admin_login_page(client):
    response = client.get('/admin/login')
    assert response.status_code == 200