from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class EmailProviderConfig(BaseSettings):
    EMAIL_PROVIDER_NAME: str = Field(default="brevo", alias="EMAIL_PROVIDER_NAME")
    EMAIL_PROVIDER_API_KEY: str = Field(default="brevo", alias="EMAIL_PROVIDER_API_KEY")
    EMAIL_PROVIDER_BASE_URL: str = Field(default="brevo", alias="EMAIL_PROVIDER_BASE_URL")


class SMTPConfig(BaseSettings):
    SMTP_DEBUG: bool = Field(default=False, alias="SMTP_DEBUG")
    SMTP_PORT: int = Field(default=587, alias="SMTP_PORT")
    SMTP_TIMEOUT: int = Field(default=10, alias="SMTP_TIMEOUT")
    SMTP_USE_SSL: bool = Field(default=False, alias="SMTP_USE_SSL")
    SMTP_PASSWORD: str = Field(default="p@55w0rd", alias="SMTP_PASSWORD")
    SMTP_SERVER: str = Field(default="smtp.gmail.com", alias="SMTP_SERVER")
    SMTP_USERNAME: str = Field(default="admin@localhost.com", alias="SMTP_USERNAME")


@lru_cache
def smtp_config() -> SMTPConfig:
    return SMTPConfig()


smtpconfig = smtp_config()
