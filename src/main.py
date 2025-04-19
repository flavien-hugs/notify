from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.config import settings
from src.endpoints import router


@asynccontextmanager
async def lifespan(instance: FastAPI): ...


app: FastAPI = FastAPI(
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
