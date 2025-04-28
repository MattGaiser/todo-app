import pytest
from app import schemas, crud
from datetime import date
from fastapi import HTTPException

def test_get_todos(db_session):
    todos = crud.get_todos(db_session)
    assert isinstance(todos, list)

def test_get_todo(db_session, sample_todo):
    todo = crud.get_todo(db_session, sample_todo.id)
    assert todo.id == sample_todo.id
    assert todo.title == sample_todo.title
    assert todo.description == sample_todo.description
    assert todo.due_date == sample_todo.due_date
    assert todo.is_completed == sample_todo.is_completed

def test_get_todo_no_date(db_session, no_date_todo):
    todo = crud.get_todo(db_session, no_date_todo.id)
    assert todo.id == no_date_todo.id
    assert todo.title == no_date_todo.title
    assert todo.description == no_date_todo.description
    assert todo.due_date is None
    assert todo.is_completed == no_date_todo.is_completed

def test_get_todo_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        crud.get_todo(db_session, 999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Todo with id 999 not found"

def test_create_todo(db_session):
    todo_data = schemas.TodoCreate(
        title="New Todo",
        description="New Description",
        due_date=date(2024, 12, 31)
    )
    todo = crud.create_todo(db_session, todo_data)
    assert todo.title == "New Todo"
    assert todo.description == "New Description"
    assert todo.due_date == date(2024, 12, 31)
    assert todo.is_completed is False

def test_create_todo_no_date(db_session):
    todo_data = schemas.TodoCreate(
        title="New Todo No Date",
        description="New Description No Date"
    )
    todo = crud.create_todo(db_session, todo_data)
    assert todo.title == "New Todo No Date"
    assert todo.description == "New Description No Date"
    assert todo.due_date is None
    assert todo.is_completed is False

def test_create_todo_empty_date(db_session):
    todo_data = schemas.TodoCreate(
        title="New Todo Empty Date",
        description="New Description Empty Date",
        due_date=""
    )
    todo = crud.create_todo(db_session, todo_data)
    assert todo.title == "New Todo Empty Date"
    assert todo.description == "New Description Empty Date"
    assert todo.due_date is None
    assert todo.is_completed is False

def test_update_todo(db_session, sample_todo):
    update_data = schemas.TodoUpdate(
        title="Updated Todo",
        description="Updated Description"
    )
    todo = crud.update_todo(db_session, sample_todo.id, update_data)
    assert todo.id == sample_todo.id
    assert todo.title == "Updated Todo"
    assert todo.description == "Updated Description"
    assert todo.due_date == sample_todo.due_date
    assert todo.is_completed == sample_todo.is_completed

def test_update_todo_remove_date(db_session, sample_todo):
    update_data = schemas.TodoUpdate(
        title="Updated Todo",
        description="Updated Description",
        due_date=None
    )
    todo = crud.update_todo(db_session, sample_todo.id, update_data)
    assert todo.id == sample_todo.id
    assert todo.title == "Updated Todo"
    assert todo.description == "Updated Description"
    assert todo.due_date is None
    assert todo.is_completed == sample_todo.is_completed

def test_update_todo_empty_date(db_session, sample_todo):
    update_data = schemas.TodoUpdate(
        title="Updated Todo",
        description="Updated Description",
        due_date=""
    )
    todo = crud.update_todo(db_session, sample_todo.id, update_data)
    assert todo.id == sample_todo.id
    assert todo.title == "Updated Todo"
    assert todo.description == "Updated Description"
    assert todo.due_date is None
    assert todo.is_completed == sample_todo.is_completed

def test_update_todo_add_date(db_session, no_date_todo):
    update_data = schemas.TodoUpdate(
        title="Updated Todo",
        description="Updated Description",
        due_date=date(2024, 12, 31)
    )
    todo = crud.update_todo(db_session, no_date_todo.id, update_data)
    assert todo.id == no_date_todo.id
    assert todo.title == "Updated Todo"
    assert todo.description == "Updated Description"
    assert todo.due_date == date(2024, 12, 31)
    assert todo.is_completed == no_date_todo.is_completed

def test_update_todo_not_found(db_session):
    update_data = schemas.TodoUpdate(title="Updated Todo")
    with pytest.raises(HTTPException) as exc_info:
        crud.update_todo(db_session, 999, update_data)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Todo with id 999 not found"

def test_delete_todo(db_session, sample_todo):
    result = crud.delete_todo(db_session, sample_todo.id)
    assert result["message"] == "Todo deleted successfully"
    with pytest.raises(HTTPException) as exc_info:
        crud.get_todo(db_session, sample_todo.id)
    assert exc_info.value.status_code == 404

def test_delete_todo_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        crud.delete_todo(db_session, 999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Todo with id 999 not found"

def test_complete_todo(db_session, sample_todo):
    todo = crud.complete_todo(db_session, sample_todo.id)
    assert todo.id == sample_todo.id
    assert todo.is_completed is True

def test_complete_todo_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        crud.complete_todo(db_session, 999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Todo with id 999 not found"

def test_incomplete_todo(db_session, completed_todo):
    todo = crud.incomplete_todo(db_session, completed_todo.id)
    assert todo.id == completed_todo.id
    assert todo.is_completed is False

def test_incomplete_todo_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        crud.incomplete_todo(db_session, 999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Todo with id 999 not found" 