from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination

from src.common.config.setup_permission import __load_app_description, BASE_DIR
from src.common.helpers.exception import setup_exception_handlers
from src.config import settings, shutdown_handler, startup_handler
from src.endpoints import router
from src.models import Notify


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_handler(app, [Notify])
    yield
    await shutdown_handler(app)


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


@app.get(
    "/_permissions",
    response_model=dict,
    summary="Get app description and permissions",
    status_code=200,
    include_in_schema=False,
)
async def read_permissions() -> dict:
    filepath = BASE_DIR / "appdesc.yml"
    data = await __load_app_description(filepath)
    return data[0]


add_pagination(app)
app.include_router(router=router)
setup_exception_handlers(app)
