import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import Base, engine, get_db
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService

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
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
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


@pytest.fixture
def created_todo(client):
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "Test Description",
            "due_date": "2025-04-01"
        }
    )
    return response.json()


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


def test_get_todos(client, created_todo):
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Todo"
    assert data[0]["description"] == "Test Description"
    assert data[0]["due_date"] == "2025-04-01"
    assert data[0]["is_completed"] == False


def test_get_todo(client, created_todo):
    response = client.get(f"/todos/{created_todo['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["due_date"] == "2025-04-01"
    assert data["is_completed"] == False


def test_update_todo(client, created_todo):
    response = client.put(
        f"/todos/{created_todo['id']}",
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


def test_delete_todo(client, created_todo):
    response = client.delete(f"/todos/{created_todo['id']}")
    assert response.status_code == 204

    response = client.get(f"/todos/{created_todo['id']}")
    assert response.status_code == 404


def test_complete_todo(client, created_todo):
    response = client.patch(f"/todos/{created_todo['id']}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] == True


def test_incomplete_todo(client, created_todo):
    response = client.patch(f"/todos/{created_todo['id']}/complete")
    assert response.status_code == 200
    assert response.json()["is_completed"] == True

    response = client.patch(f"/todos/{created_todo['id']}/incomplete")
    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] == False 
