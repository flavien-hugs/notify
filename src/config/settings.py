from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class NotifyBaseConfig(BaseSettings):
    APP_NAME: Optional[str] = Field(default="notify", alias="APP_NAME", description="Name of the application")
    APP_TITLE: Optional[str] = Field(default="UNSTA: Notify System", alias="APP_TITLE",
                                     description="Title of the application")
    APP_DOCS_URL: Optional[str] = Field(default="/api/notify/docs", alias="APP_DOCS_URL",
                                        description="The URL of the documentation")
    APP_OPENAPI_URL: Optional[str] = Field(
        default="/api/notify/openapi.json", alias="APP_OPENAPI_URL", description="The URL of the OpenAPI schema"
    )
    APP_HOSTNAME: Optional[str] = Field(default="localhost", alias="APP_HOSTNAME",
                                        description="Hostname of the application")
    APP_PORT: Optional[int] = Field(default=9090, alias="APP_PORT",
                                            description="Default port of the application")
    APP_LOOP: Optional[str] = Field(
        default="uvloop", alias="APP_LOOP", description="Type of loop to use: none, auto, asyncio or uvloop"
    )
    APP_ENVIRONMENT: Optional[str] = Field(
        default="dev",
        alias="APP_ENVIRONMENT",
        description="The environment where the application is running (staging, preprod, prod, dev)",
    )


@lru_cache
def get_settings() -> NotifyBaseConfig:
    return NotifyBaseConfig()
