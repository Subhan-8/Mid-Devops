import pytest
from ssis import create_app
from ssis.models.admin import Admin
import os

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'MYSQL_HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'MYSQL_USER': os.getenv('MYSQL_USER', 'ssis_user'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD', 'ssis_password'),
        'MYSQL_DB': os.getenv('MYSQL_DATABASE', 'ssisdb')
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