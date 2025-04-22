from typing import List, Type

from beanie import Document, init_beanie
from fastapi import FastAPI

from src.common.config.mongo_client import config_mongodb_client
from src.common.discovery.consul import deregister_service, register_service
from .settings import get_settings


async def startup_handler(instance: FastAPI, models: List[Type[Document]]):
    settings = get_settings()

    client = await config_mongodb_client(settings.MONGODB_URI)
    if instance:
        instance.mongo_db_client = client

    db_name = settings.NOTIFY_DB_PATH.split(".", maxsplit=1)[0]
    await init_beanie(database=client[db_name], document_models=models)

    # Register app endpoints to consul
    register_service(
        service_name=settings.APP_NAME,
        service_port=settings.APP_PORT,
        consul_host=settings.CONSUL_HOST,
        consul_port=settings.CONSUL_PORT,
        health_check_endpoint="/@ping",
    )


async def shutdown_handler(instance: FastAPI):
    settings = get_settings()

    if hasattr(instance, "mongo_db_client"):
        instance.mongo_db_client.close()

    # de-register app endpoints to consul
    deregister_service(settings.APP_NAME, settings.CONSUL_HOST, settings.CONSUL_PORT)
