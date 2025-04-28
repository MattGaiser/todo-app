import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import Base, engine, get_db
from app.models import Todo
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService
from datetime import datetime, date

# Create test database
Base.metadata.create_all(bind=engine)

def get_test_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_database():
    # Clean up before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up after each test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    return next(get_test_db())

@pytest.fixture
def repository(db):
    return TodoRepository(db)

@pytest.fixture
def service(repository):
    return TodoService(repository)

def test_create_todo(client, db):
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["due_date"] == "2025-04-01"
    assert data["is_completed"] == False

def test_get_todos(client, db):
    # Create a todo first
    client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Todo"
    assert data[0]["description"] == "Test Description"
    assert data[0]["due_date"] == "2025-04-01"
    assert data[0]["is_completed"] == False

def test_get_todo(client, db):
    # Create a todo first
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    todo_id = response.json()["id"]
    
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["due_date"] == "2025-04-01"
    assert data["is_completed"] == False

def test_update_todo(client, db):
    # Create a todo first
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    todo_id = response.json()["id"]
    
    response = client.put(
        f"/todos/{todo_id}",
        json={
            "title": "Updated Todo",
            "description": "Updated Description",
            "due_date": "2025-04-02"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["due_date"] == "2025-04-02"
    assert data["is_completed"] == False

def test_delete_todo(client, db):
    # Create a todo first
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    todo_id = response.json()["id"]
    
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    
    # Verify todo is deleted
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404

def test_complete_todo(client, db):
    # Create a todo first
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    todo_id = response.json()["id"]
    
    response = client.patch(f"/todos/{todo_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] == True

def test_incomplete_todo(client, db):
    # Create a todo first
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    todo_id = response.json()["id"]
    
    # Complete the todo
    response = client.patch(f"/todos/{todo_id}/complete")
    assert response.status_code == 200
    assert response.json()["is_completed"] == True
    
    # Now test incomplete
    response = client.patch(f"/todos/{todo_id}/incomplete")
    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] == False 