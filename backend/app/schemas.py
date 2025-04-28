from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime, date

def validate_due_date(v):
    if v == "":
        return None
    return v

def validate_title(v):
    if not v or not v.strip():
        raise ValueError("Title cannot be empty")
    return v.strip()

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None

    _validate_due_date = field_validator('due_date', mode='before')(validate_due_date)
    _validate_title = field_validator('title', mode='before')(validate_title)

class TodoCreate(TodoBase):
    model_config = ConfigDict(from_attributes=True)

class TodoUpdate(TodoBase):
    title: Optional[str] = None
    is_completed: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)

class Todo(TodoBase):
    id: int
    is_completed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
