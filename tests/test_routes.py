import os
import sys
import pytest
import mysql.connector as mysql

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ssis import create_app

@pytest.fixture(scope='session')
def db_connection(database_config):
    """Create a test database connection"""
    try:
        connection = mysql.connect(**database_config)
        yield connection
        connection.close()
    except mysql.Error as err:
        pytest.fail(f"Failed to connect to database: {err}")


@pytest.fixture()
def app(db_connection):
    """
    Create Flask app with test DB injected.
    Each test gets isolated transactions via rollback.
    """
    app = create_app(test_db=db_connection)
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
    """Test the main landing page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data or b"SSIS" in response.data

def test_admin_login_page(client):
    """Test admin login page access"""
    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b"Login" in response.data or b"Admin" in response.data

def test_admin_login(client, db_connection):
    """Test admin login functionality"""
    # Test with correct credentials
    response = client.post('/admin/login', data={
        'username': 'test_admin',
        'password': 'test_password'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_college_list(client):
    """Test college listing page"""
    response = client.get('/colleges/')
    assert response.status_code == 200
    assert b"COL1" in response.data and b"Test College" in response.data

def test_course_list(client):
    """Test course listing page"""
    response = client.get('/courses/')
    assert response.status_code == 200
    assert b"CRS1" in response.data and b"Test Course" in response.data

def test_student_list(client):
    """Test student listing page"""
    response = client.get('/students/')
    assert response.status_code == 200
    assert b"2021-0001" in response.data and b"Test Student" in response.data

def test_404_page(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
