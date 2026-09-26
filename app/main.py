from fastapi import FastAPI

from app.routers.recommendation_router import router as recommendation_router

from fastapi.exceptions import RequestValidationError

from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    unexpected_exception_handler,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Product Recommendation System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommendation_router)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)