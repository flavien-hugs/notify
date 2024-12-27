from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class NotifyBaseConfig(BaseSettings):
    APP_NAME: Optional[str] = Field(default="notify", alias="APP_NAME", description="Name of the application")
    APP_TITLE: Optional[str] = Field(default="UNSTA: Notify System", alias="APP_TITLE",
                                     description="Title of the application")
    APP_HOSTNAME: Optional[str] = Field(default="localhost", alias="APP_HOSTNAME",
                                        description="Hostname of the application")
    APP_RELOAD: Optional[bool] = Field(default=True, alias="APP_RELOAD", description="Enable/Disable auto-reload")
    APP_LOG_LEVEL: Optional[str] = Field(default="debug", alias="APP_LOG_LEVEL",
                                         description="Log level of the application")
    APP_ACCESS_LOG: Optional[bool] = Field(default=True, alias="APP_ACCESS_LOG",
                                           description="Enable/Disable access log")
    APP_DEFAULT_PORT: Optional[int] = Field(default=8090, alias="APP_DEFAULT_PORT",
                                            description="Default port of the application")
    APP_LOOP: Optional[str] = Field(
        default="uvloop", alias="APP_LOOP", description="Type of loop to use: none, auto, asyncio or uvloop"
    )


@lru_cache
def get_settings() -> NotifyBaseConfig:
    return NotifyBaseConfig()
