import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_todo(client):
    response = client.post('/api/todos', 
                          json={'title': 'Test Todo'})
    assert response.status_code == 201
    assert response.json['title'] == 'Test Todo'

def test_get_todos(client):
    # Create a todo first
    client.post('/api/todos', json={'title': 'Test Todo'})
    response = client.get('/api/todos')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_update_todo(client):
    # Create todo
    create_response = client.post('/api/todos', json={'title': 'Test Todo'})
    todo_id = create_response.json['id']
    
    # Update it
    response = client.put(f'/api/todos/{todo_id}', 
                         json={'completed': True})
    assert response.status_code == 200
    
    # Verify update
    get_response = client.get('/api/todos')
    updated_todo = next(t for t in get_response.json if t['id'] == todo_id)
    assert updated_todo['completed'] == True

def test_delete_todo(client):
    # Create todo
    create_response = client.post('/api/todos', json={'title': 'Test Todo'})
    todo_id = create_response.json['id']
    
    # Delete it
    response = client.delete(f'/api/todos/{todo_id}')
    assert response.status_code == 200