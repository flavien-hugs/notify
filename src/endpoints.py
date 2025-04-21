from typing import Literal, Union

from fastapi import APIRouter, Body, Query, status, Depends
from fastapi_pagination.ext.beanie import paginate
from pymongo import ASCENDING, DESCENDING

from src.common.helpers.pagination import customize_page
from src.config import settings
from src.models import Notify
from src.schemas import EmailPayload, FilterNotify, SMSPayload
from src.shared import select_provider

router = APIRouter(
    prefix="",
    tags=["NOTIFY"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("/notifications", response_model=customize_page(Notify), status_code=status.HTTP_200_OK)
async def read_all(filter: FilterNotify = Depends(FilterNotify), sort: Literal["desc", "asc"] = Query(default=None)):
    search = filter.model_dump(exclude_unset=True)

    if filter.notify_type:
        search.update({"notify_type": filter.notify_type})

    if filter.status:
        search.update({"status": filter.status})

    sorted = DESCENDING if sort == desc else ASCENDING
    cursor = Notify.find(search, sort=[("created_at", sorted)])

    return await paginate(cursor)


@router.post("/send", response_model=Notify, summary="Send Message", status_code=status.HTTP_200_OK)
async def send(type: Literal["sms", "email", "push"], payload: Union[SMSPayload, EmailPayload] = Body(...)):
    match type:
        case value if value == "email":
            provider = select_provider(settings.NOTIFY_EMAIL_PROVIDER_CLASS)
            return await provider.send(**payload.model_dump(), model_klass=Notify)
        case value if value == "sms":
            provider = select_provider(settings.NOTIFY_SMS_PROVIDER_CLASS)
            return await provider.send(**payload.model_dump(), model_klass=Notify)
        case value if value == "push":
            return None
        case _:
            return None
