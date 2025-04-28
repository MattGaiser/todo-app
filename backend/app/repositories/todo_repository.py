from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, todo: TodoCreate) -> Todo:
        db_todo = Todo(**todo.model_dump())
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def get_all(self) -> List[Todo]:
        return self.db.query(Todo).all()

    def update(self, todo_id: int, todo: TodoUpdate) -> Optional[Todo]:
        db_todo = self.get_by_id(todo_id)
        if db_todo:
            for key, value in todo.model_dump(exclude_unset=True).items():
                setattr(db_todo, key, value)
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo

    def delete(self, todo_id: int) -> bool:
        db_todo = self.get_by_id(todo_id)
        if db_todo:
            self.db.delete(db_todo)
            self.db.commit()
            return True
        return False

    def complete(self, todo_id: int) -> Optional[Todo]:
        db_todo = self.get_by_id(todo_id)
        if db_todo:
            db_todo.is_completed = True
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo

    def incomplete(self, todo_id: int) -> Optional[Todo]:
        db_todo = self.get_by_id(todo_id)
        if db_todo:
            db_todo.is_completed = False
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo 