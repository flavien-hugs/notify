from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class SMSConfig(BaseSettings):
    SMS_SENDER: str = Field(default="sms", alias="SMS_SENDER")
    SMS_API_KEY: str = Field(default="sms", alias="SMS_API_KEY")
    SMS_BASE_URL: str = Field(default="sms", alias="SMS_BASE_URL")
    SMS_CLIENT_ID: str = Field(default="sms", alias="SMS_CLIENT_ID")
    SMS_TYPE: Optional[str] = Field(default="sms", alias="SMS_TYPE")


@lru_cache
def sms_config() -> SMSConfig:
    return SMSConfig()


smsconfig = sms_config()
