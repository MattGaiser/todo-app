import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import Todo
from datetime import datetime, date

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_todo(db_session):
    todo = Todo(
        title="Test Todo",
        description="Test Description",
        due_date=date(2024, 12, 31),
        is_completed=False,
        created_at=datetime.utcnow()
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

@pytest.fixture
def no_date_todo(db_session):
    todo = Todo(
        title="No Date Todo",
        description="No Date Description",
        is_completed=False,
        created_at=datetime.utcnow()
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

@pytest.fixture
def completed_todo(db_session):
    todo = Todo(
        title="Completed Todo",
        description="Completed Description",
        due_date=date(2024, 12, 31),
        is_completed=True,
        created_at=datetime.utcnow()
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo 