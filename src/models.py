from datetime import datetime, UTC

import pymongo
from beanie import Document
from dotenv.variables import Literal
from pydantic import Field

from src.config import settings


class Notify(Document):
    status: Literal["pending", "successful", "failed"] = Field(default="pending")
    notify_type: Literal["sms", "email", "push"] = Field(default="email")
    created_at: datetime = Field(default=datetime.now(UTC))

    class Settings:
        use_revision = True
        name = settings.NOTIFY_DB_PATH.split(".", maxsplit=1)[-1]
        indexes = [
            pymongo.IndexModel(
                [("created_at", -1), ("status", 1)],
                background=True,
            )
        ]
