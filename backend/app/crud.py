from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from pydantic import ValidationError

def get_todos(db: Session):
    return db.query(models.Todo).all()

def get_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return todo

def create_todo(db: Session, todo: schemas.TodoCreate):
    try:
        db_todo = models.Todo(**todo.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    try:
        db_todo = get_todo(db, todo_id)
        for key, value in todo.model_dump(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

def delete_all_todos(db: Session):
    db.query(models.Todo).delete()
    db.commit()
    return {"message": "All todos deleted successfully"}

def complete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    db_todo.is_completed = True
    db.commit()
    db.refresh(db_todo)
    return db_todo

def incomplete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    db_todo.is_completed = False
    db.commit()
    db.refresh(db_todo)
    return db_todo
