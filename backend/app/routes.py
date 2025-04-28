from fastapi import APIRouter, Depends, Response, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app import schemas
from app.database import get_db
from app.services.todo_service import TodoService
from app.repositories.todo_repository import TodoRepository

router = APIRouter()

def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    repository = TodoRepository(db)
    return TodoService(repository)

@router.get("/todos", response_model=List[schemas.Todo])
def list_todos(service: TodoService = Depends(get_todo_service)):
    return service.get_all_todos()

@router.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    try:
        return service.get_todo(todo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, service: TodoService = Depends(get_todo_service)):
    try:
        return service.create_todo(todo)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, service: TodoService = Depends(get_todo_service)):
    try:
        return service.update_todo(todo_id, todo)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    try:
        if service.delete_todo(todo_id):
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/todos", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_todos(service: TodoService = Depends(get_todo_service)):
    service.delete_all_todos()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/todos/{todo_id}/complete", response_model=schemas.Todo)
def complete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    try:
        return service.complete_todo(todo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/todos/{todo_id}/incomplete", response_model=schemas.Todo)
def incomplete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    try:
        return service.incomplete_todo(todo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
