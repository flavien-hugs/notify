from typing import List, Type

from beanie import Document, init_beanie
from fastapi import FastAPI

from src.common.config.mongo_client import config_mongodb_client
from .settings import get_settings


async def startup_handler(instance: FastAPI, models: List[Type[Document]]):
    settings = get_settings()

    client = await config_mongodb_client(settings.MONGODB_URI)
    if instance:
        instance.mongo_db_client = client

    db_name = settings.NOTIFY_DB_PATH.split(".", maxsplit=1)[0]
    await init_beanie(database=client[db_name], document_models=models)


async def shutdown_handler(instance: FastAPI):
    if hasattr(instance, "mongo_db_client"):
        instance.mongo_db_client.close()
