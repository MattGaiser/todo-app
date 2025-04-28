# Todo Application

A full-stack todo application with a modern React frontend and FastAPI backend, containerized with Docker.

## Technologies Used

### Frontend
- React with TypeScript
- Vite for build tooling
- Modern CSS with responsive design
- React Hooks for state management
- Memoization for performance optimization

### Backend
- FastAPI (Python)
- SQLAlchemy for ORM
- PostgreSQL database
- Pydantic for data validation

### Infrastructure
- Docker and Docker Compose for containerization
- PostgreSQL for data persistence

## Key Features

- ✅ Create, read, update, and delete todo items
- ✅ Mark todos as complete/incomplete
- ✅ Optional due dates and descriptions
- ✅ Filter todos by status (all/completed/incomplete/overdue)
- ✅ Sort todos by due date, creation date, or title
- ✅ Responsive design for all screen sizes
- ✅ Input validation and error handling
- ✅ Persistent storage with PostgreSQL
- ✅ Containerized deployment

## Design Choice Discussion

### Design choices I made

#### Frontend
- I just used the default React state management as the app is small
- Just used simple AI generated CSS as I did not wish to fuss with a design library
- Did some performance optimizations with memoization. 
- Implemented the sorting and filtering on the frontend to reduce API calls to the backend. Opinions differ on this. I think it is reasonable for a simple Todo app as the number of items would never be excessively large and I would rather outsource the CPU cycles to be paid by the user and keep my API requests within the free tier as much as possible.

#### Backend
- Implemented full database models and used FastAPI to quickly put together some endpoints to work with them. Used Pydantic to validate the data. 
- I skipped migration support as this is not going to be expanded, but something like Alembic would be beneficial in a real project. 
- The project structure is well-organized with clear separation of concerns, featuring a modular design that separates routes, models, repositories, and middleware. 
- The API design adheres to RESTful principles with proper HTTP method usage and consistent response formats. 
- The database integration is solid, using SQLAlchemy ORM with proper model definitions. 
- The architecture is extreme overkill for this trivial app, particularly the respository and service layers, but for anything more complex there would be benefit to having it. I want you to know that I know, so a lot of overengineering has been done for this app. 


### Things I deliberately left out for lack of time
- This is dockerized, but it is not production ready. It just serves it on the vite server for example. There is no production setup. Dockerization is simply so you can run it in one step. 
- I hardcoded variables in the Docker files rather than having you fumble with an env file.
- Skipped on most security. There is no authentication.  Wildcard for the CORS values. No rate limiting on the API. 
- No logging, no Sentry, no user analytics, no API versioning, no linting, etc. Well, I don't expect to be doing much work on this later on, so those quality of life additions are not required. 
- Ran out of time for frontend tests and things like test coverage reporting and caching. 
- Just used simple CSS that is AI generated. Didn't want to fuss with Material MUI too much with the time limit. 

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Git for version control

### Running the Application

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-app
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

This will start:
- Frontend on http://localhost:5173
- Backend API on http://localhost:8000
- PostgreSQL database on port 5432

### Development

The application is set up for development with hot-reloading:
- Frontend changes will automatically reload
- Backend changes will automatically reload
- Database data persists between restarts

### Running Tests

The backend tests are containerized separately. To run them:

```bash
cd backend
docker-compose -f docker-compose.test.yml up --build
```

This will:
- Build a separate test container
- Run the backend tests

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
todo-app/
├── frontend/                # React frontend application
│   ├── src/                # Source code
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── hooks/         # Custom React hooks
│   │   ├── App.tsx        # Main application component
│   │   ├── App.css        # Main application styles
│   │   ├── api.ts         # API client
│   │   ├── types.ts       # TypeScript type definitions
│   │   └── main.tsx       # Application entry point
│   ├── Dockerfile         # Frontend container configuration
│   ├── Dockerfile.test    # Frontend test container configuration
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.ts     # Vite configuration
│   └── playwright.config.ts # Playwright test configuration
├── backend/                # FastAPI backend application
│   ├── app/               # Backend source code
│   │   ├── repositories/  # Data access layer
│   │   ├── services/      # Business logic layer
│   │   ├── middleware/    # Request/response middleware
│   │   ├── main.py        # Application entry point
│   │   ├── routes.py      # API route definitions
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── crud.py        # CRUD operations
│   │   └── database.py    # Database configuration
│   ├── tests/             # Backend tests
│   │   ├── test_api.py    # API endpoint tests
│   │   ├── test_crud.py   # CRUD operation tests
│   │   ├── test_models.py # Model tests
│   │   └── test_todos.py  # Todo-specific tests
│   ├── Dockerfile         # Backend container configuration
│   ├── Dockerfile.test    # Backend test container configuration
│   ├── requirements.txt   # Backend dependencies
│   └── pytest.ini        # Pytest configuration
├── docker-compose.yml     # Main Docker configuration
└── docker-compose.test.yml # Test Docker configuration
```
## License

This project is licensed under the MIT License - see the LICENSE file for details. 
