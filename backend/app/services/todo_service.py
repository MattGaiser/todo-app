from typing import List, Optional
from datetime import datetime
from pydantic import ValidationError
from app.repositories.todo_repository import TodoRepository
from app.schemas import TodoCreate, TodoUpdate
from app.models import Todo

class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def create_todo(self, todo: TodoCreate) -> Todo:
        try:
            if not todo.title.strip():
                raise ValidationError("Title cannot be empty", model=TodoCreate)
            return self.repository.create(todo)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValueError(str(e))

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"Todo with id {todo_id} not found")
        return todo

    def get_all_todos(self) -> List[Todo]:
        return self.repository.get_all()

    def update_todo(self, todo_id: int, todo: TodoUpdate) -> Todo:
        if not self.repository.get_by_id(todo_id):
            raise ValueError(f"Todo with id {todo_id} not found")
        
        try:
            updated_todo = self.repository.update(todo_id, todo)
            if not updated_todo:
                raise ValueError(f"Failed to update todo with id {todo_id}")
            return updated_todo
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValueError(str(e))

    def delete_todo(self, todo_id: int) -> bool:
        if not self.repository.get_by_id(todo_id):
            raise ValueError(f"Todo with id {todo_id} not found")
        return self.repository.delete(todo_id)

    def complete_todo(self, todo_id: int) -> Todo:
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"Todo with id {todo_id} not found")
        if todo.is_completed:
            raise ValueError(f"Todo with id {todo_id} is already completed")
        
        completed_todo = self.repository.complete(todo_id)
        if not completed_todo:
            raise ValueError(f"Failed to complete todo with id {todo_id}")
        return completed_todo

    def incomplete_todo(self, todo_id: int) -> Todo:
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"Todo with id {todo_id} not found")
        if not todo.is_completed:
            raise ValueError(f"Todo with id {todo_id} is already incomplete")
        
        incomplete_todo = self.repository.incomplete(todo_id)
        if not incomplete_todo:
            raise ValueError(f"Failed to mark todo with id {todo_id} as incomplete")
        return incomplete_todo 