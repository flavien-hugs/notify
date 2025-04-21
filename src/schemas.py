from typing import List, Optional, Union, Literal
from dataclasses import dataclass
from pydantic import BaseModel, EmailStr, Field


class BaseNotifyModel(BaseModel):
    to: Union[EmailStr, str]
    body: str
    recipients: List[Union[EmailStr, str]]


class EmailPayload(BaseNotifyModel):
    subject: str
    hidden_copy: Optional[List[EmailStr]] = None


class SMSPayload(BaseModel):
    message: str = Field(default=..., description="Message to send")
    recipient: str = Field(default=..., description="Phone number to send message")


class FilterNotify(BaseModel):
    notify_type: Optional[Literal["sms", "email", "push"]] = Field(default=None)
    status: Optional[Literal["pending", "successful", "failed"]] = Field(default=None)
