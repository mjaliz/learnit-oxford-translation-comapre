import os
import sys
from tempfile import NamedTemporaryFile
from loguru import logger
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    File,
    Form,
    UploadFile,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from app.api.routes import meaining


app = FastAPI(
    title="learnit-oxford-translation",
    docs_url=os.getenv("SWAGGER_URL"),
    redoc_url=os.getenv("REDOC_URL"),
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "message": {"text": str(exc.detail)}, "data": None},
    )


app.include_router(meaining.router)
app.mount("/", StaticFiles(directory="statics", html=True), name="statics")
