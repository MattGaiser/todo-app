import pytest
from app.models import Todo
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError

def test_todo_model():
    todo = Todo(
        title="Test Todo",
        description="Test Description",
        due_date=date(2024, 12, 31),
        is_completed=False,
        created_at=datetime.utcnow()
    )
    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.due_date == date(2024, 12, 31)
    assert todo.is_completed == False
    assert todo.created_at is not None

def test_todo_model_without_due_date():
    todo = Todo(
        title="Test Todo",
        description="Test Description",
        is_completed=False,
        created_at=datetime.utcnow()
    )
    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.due_date is None
    assert todo.is_completed == False
    assert todo.created_at is not None

def test_todo_model_with_completed():
    todo = Todo(
        title="Test Todo",
        description="Test Description",
        due_date=date(2024, 12, 31),
        is_completed=True,
        created_at=datetime.utcnow()
    )
    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.due_date == date(2024, 12, 31)
    assert todo.is_completed == True
    assert todo.created_at is not None

def test_todo_model_defaults():
    todo = Todo(title="Test Todo")
    assert todo.title == "Test Todo"
    assert todo.description is None
    assert todo.due_date is None
    assert todo.is_completed is False
    assert isinstance(todo.created_at, datetime)

def test_todo_model_required_fields(db_session):
    with pytest.raises(IntegrityError):
        todo = Todo()
        db_session.add(todo)
        db_session.commit() 