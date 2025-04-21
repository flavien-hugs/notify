from datetime import datetime, UTC
from typing import Any, Dict, Literal, Optional

import pymongo
from beanie import Document
from pydantic import Field

from src.config import settings


class Notify(Document):
    notify_type: Literal["sms", "email", "push"] = Field(default=None)
    status: Literal["pending", "successful", "failed"] = Field(default=None)
    data: Optional[Dict[str, Any]] = Field(default=dict)
    created_at: Optional[datetime] = Field(default=datetime.now(UTC))

    class Settings:
        use_revision = True
        name = settings.NOTIFY_DB_PATH.split(".", maxsplit=1)[-1]
        indexes = [
            pymongo.IndexModel(
                [("created_at", -1), ("status", 1)],
                background=True,
            )
        ]
