from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr


class BasePayload(BaseModel):
    to: Union[EmailStr, str]
    body: str
    recipients: List[Union[EmailStr, str]]


class EmailPayload(BasePayload):
    subject: str
    hidden_copy: Optional[List[EmailStr]] = None
