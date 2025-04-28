from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_todos(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todo(client, sample_todo):
    response = client.get(f"/todos/{sample_todo.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo.id
    assert data["title"] == sample_todo.title
    assert data["description"] == sample_todo.description
    assert data["due_date"] == sample_todo.due_date.isoformat() if sample_todo.due_date else None
    assert data["is_completed"] == sample_todo.is_completed

def test_get_todo_no_date(client, no_date_todo):
    response = client.get(f"/todos/{no_date_todo.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == no_date_todo.id
    assert data["title"] == no_date_todo.title
    assert data["description"] == no_date_todo.description
    assert data["due_date"] is None
    assert data["is_completed"] == no_date_todo.is_completed

def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo with id 999 not found"

def test_create_todo(client):
    response = client.post(
        "/todos",
        json={
            "title": "New Todo",
            "description": "New Description",
            "due_date": "2024-12-31"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Todo"
    assert data["description"] == "New Description"
    assert data["due_date"] == "2024-12-31"
    assert data["is_completed"] is False

def test_create_todo_no_date(client):
    response = client.post(
        "/todos",
        json={
            "title": "New Todo No Date",
            "description": "New Description No Date"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Todo No Date"
    assert data["description"] == "New Description No Date"
    assert data["due_date"] is None
    assert data["is_completed"] is False

def test_create_todo_empty_date(client):
    response = client.post(
        "/todos",
        json={
            "title": "New Todo Empty Date",
            "description": "New Description Empty Date",
            "due_date": ""
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Todo Empty Date"
    assert data["description"] == "New Description Empty Date"
    assert data["due_date"] is None
    assert data["is_completed"] is False

def test_create_todo_validation(client):
    response = client.post(
        "/todos",
        json={
            "title": "",  # Empty title should fail
            "description": "Test Description"
        }
    )
    assert response.status_code == 422

def test_update_todo(client, sample_todo):
    response = client.put(
        f"/todos/{sample_todo.id}",
        json={
            "title": "Updated Todo",
            "description": "Updated Description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo.id
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["due_date"] == sample_todo.due_date.isoformat() if sample_todo.due_date else None
    assert data["is_completed"] == sample_todo.is_completed

def test_update_todo_remove_date(client, sample_todo):
    response = client.put(
        f"/todos/{sample_todo.id}",
        json={
            "title": "Updated Todo",
            "description": "Updated Description",
            "due_date": None
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo.id
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["due_date"] is None
    assert data["is_completed"] == sample_todo.is_completed

def test_update_todo_empty_date(client, sample_todo):
    response = client.put(
        f"/todos/{sample_todo.id}",
        json={
            "title": "Updated Todo",
            "description": "Updated Description",
            "due_date": ""
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo.id
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["due_date"] is None
    assert data["is_completed"] == sample_todo.is_completed

def test_update_todo_add_date(client, no_date_todo):
    response = client.put(
        f"/todos/{no_date_todo.id}",
        json={
            "title": "Updated Todo",
            "description": "Updated Description",
            "due_date": "2024-12-31"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == no_date_todo.id
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["due_date"] == "2024-12-31"
    assert data["is_completed"] == no_date_todo.is_completed

def test_update_todo_not_found(client):
    response = client.put(
        "/todos/999",
        json={"title": "Updated Todo"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo with id 999 not found"

def test_delete_todo(client, sample_todo):
    response = client.delete(f"/todos/{sample_todo.id}")
    assert response.status_code == 204

def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo with id 999 not found"

def test_complete_todo(client, sample_todo):
    response = client.patch(f"/todos/{sample_todo.id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo.id
    assert data["is_completed"] is True

def test_complete_todo_not_found(client):
    response = client.patch("/todos/999/complete")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo with id 999 not found"

def test_incomplete_todo(client, completed_todo):
    response = client.patch(f"/todos/{completed_todo.id}/incomplete")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == completed_todo.id
    assert data["is_completed"] is False

def test_incomplete_todo_not_found(client):
    response = client.patch("/todos/999/incomplete")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo with id 999 not found" 
