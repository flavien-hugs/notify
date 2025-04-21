from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.config import settings, shutdown_handler, startup_handler
from src.common.helpers.exception import setup_exception_handlers
from src.endpoints import router
from src.models import Notify
from fastapi_pagination import add_pagination


@asynccontextmanager
async def lifespan(instance: FastAPI):
    await startup_handler(instance, [Notify])
    yield
    await shutdown_handler(instance)


app: FastAPI = FastAPI(
    lifespan=lifespan,
    title=settings.APP_TITLE,
    docs_url=settings.APP_DOCS_URL,
    openapi_url=settings.APP_OPENAPI_URL,
)


@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse(url=settings.APP_DOCS_URL)


@app.get("/@ping", tags=["DEFAULT"], summary="Check if server is available")
async def ping():
    return {"message": "pong !"}


app.include_router(router)
add_pagination(app)
setup_exception_handlers(app)
