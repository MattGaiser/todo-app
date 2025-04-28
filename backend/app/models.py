from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from datetime import datetime
from app.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'created_at' not in kwargs:
            self.created_at = datetime.utcnow()
        if 'is_completed' not in kwargs:
            self.is_completed = False
