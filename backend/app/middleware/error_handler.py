from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from typing import Union
import logging
import traceback

logger = logging.getLogger(__name__)

class ErrorHandler:
    @staticmethod
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        # Log the error
        logger.error(f"Unhandled exception: {str(exc)}")
        logger.error(traceback.format_exc())

        # Determine the status code and error message
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = "An unexpected error occurred"

        if isinstance(exc, RequestValidationError):
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            error_message = "Validation error"
        elif isinstance(exc, SQLAlchemyError):
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_message = "Database error"

        # In development, include the full error details
        if request.app.debug:
            return JSONResponse(
                status_code=status_code,
                content={
                    "error": error_message,
                    "detail": str(exc),
                    "type": exc.__class__.__name__,
                    "traceback": traceback.format_exc()
                }
            )

        # In production, return a sanitized error response
        return JSONResponse(
            status_code=status_code,
            content={
                "error": error_message
            }
        ) 