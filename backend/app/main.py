from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app import routes
from app.database import Base, engine
from .middleware.error_handler import ErrorHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return await ErrorHandler.handle_exception(request, exc)

app.include_router(routes.router)
