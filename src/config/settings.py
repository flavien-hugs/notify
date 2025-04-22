from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

# from dotenv import load_dotenv
# load_dotenv(".env")


class NotifyBaseConfig(BaseSettings):
    # CONSUL CONFIG
    CONSUL_HOST: str = Field(default="localhost", alias="CONSUL_HOST")
    CONSUL_PORT: int = Field(default=8500, alias="CONSUL_PORT")

    # APPLICATION CONFIGURATION
    APP_NAME: Optional[str] = Field(default="notify", alias="APP_NAME", description="Name of the application")
    APP_TITLE: Optional[str] = Field(default="UNSTA: Notify System", alias="APP_TITLE", description="Title of the application")
    APP_DOCS_URL: Optional[str] = Field(
        default="/api/notify/docs", alias="APP_DOCS_URL", description="The URL of the documentation"
    )
    APP_OPENAPI_URL: Optional[str] = Field(
        default="/api/notify/openapi.json", alias="APP_OPENAPI_URL", description="The URL of the OpenAPI schema"
    )
    APP_HOSTNAME: Optional[str] = Field(default="localhost", alias="APP_HOSTNAME", description="Hostname of the application")
    APP_PORT: Optional[int] = Field(default=9090, alias="APP_PORT", description="Default port of the application")
    APP_LOOP: Optional[str] = Field(
        default="uvloop", alias="APP_LOOP", description="Type of loop to use: none, auto, asyncio or uvloop"
    )
    APP_ENVIRONMENT: Optional[str] = Field(
        default="dev",
        alias="APP_ENVIRONMENT",
        description="The environment where the application is running (staging, preprod, prod, dev)",
    )

    # PROVIDER CONFIG
    NOTIFY_SMS_PROVIDER_CLASS: str = Field(
        default="src.providers.sms.SMSProvider",
        alias="NOTIFY_SMS_PROVIDER_CLASS",
        description="The class of the notify provider",
    )
    NOTIFY_EMAIL_PROVIDER_CLASS: str = Field(
        default="src.providers.email.SMTPProvider",
        alias="NOTIFY_PROVIDER_CLASS",
        description="The class of the notify provider",
    )

    # MONGODB CONFIG
    NOTIFY_DB_PATH: str = Field(default="db.notify", alias="NOTIFY_DB_PATH", description="The path to the notify db")
    MONGODB_URI: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URI", description="The MongoDB URI")


@lru_cache
def get_settings() -> NotifyBaseConfig:
    return NotifyBaseConfig()
