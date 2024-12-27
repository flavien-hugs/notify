from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.config import settings
from src.endpoint import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pass


app: FastAPI = FastAPI(
    title=f"{settings.APP_TITLE} API Service",
    docs_url=f"/{settings.APP_NAME}/docs",
    openapi_url=f"/{settings.APP_NAME}/openapi.json",
)


@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse(url=f"/{settings.APP_NAME}/docs")


@app.get(f"/{settings.APP_NAME}/@ping", tags=["DEFAULT"], summary="Check if server is available")
async def ping():
    return {"message": "pong !"}


app.include_router(router)
