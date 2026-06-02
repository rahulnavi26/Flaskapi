import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the welcome index endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Welcome" in data["message"]
    assert "endpoints" in data

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"

def test_get_all_tasks(client):
    """Test retrieving all tasks."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "tasks" in data
    assert len(data["tasks"]) >= 2

def test_get_single_task_success(client):
    """Test retrieving a single existing task."""
    response = client.get('/api/tasks/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["task"]["id"] == 1
    assert data["task"]["title"] == "Set up project"

def test_get_single_task_not_found(client):
    """Test retrieving a non-existent task."""
    response = client.get('/api/tasks/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Not Found"

def test_create_task_success(client):
    """Test creating a new task successfully."""
    payload = {
        "title": "Write Unit Tests",
        "description": "Ensure tests cover all endpoints",
        "completed": False
    }
    response = client.post(
        '/api/tasks',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["task"]["title"] == "Write Unit Tests"
    assert data["task"]["id"] is not None

def test_create_task_bad_request(client):
    """Test creating a task with missing required title."""
    payload = {
        "description": "Missing title field"
    }
    response = client.post(
        '/api/tasks',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["error"] == "Bad Request"
