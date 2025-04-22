from typing import Literal, Union

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi_pagination.ext.beanie import apaginate
from pymongo import ASCENDING, DESCENDING

from src.common.helpers.pagination import CustomPage
from src.config import settings
from src.models import Notify
from src.schemas import EmailPayload, FilterNotify, SMSPayload
from src.shared import select_provider

router = APIRouter(
    prefix="",
    tags=["NOTIFY"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/send", response_model=Notify, summary="Send Message", status_code=status.HTTP_202_ACCEPTED)
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


@router.get(
    "/notifications",
    summary="Read all notify",
    response_model_exclude={"data"},
    response_model=CustomPage[Notify],
    status_code=status.HTTP_200_OK
)
async def read(
        filter: FilterNotify = Depends(FilterNotify),
        sort: Literal["desc", "asc"] = Query(default=None)
):
    search = filter.model_dump(exclude_none=True)

    if filter.notify_type:
        search.update({"notify_type": filter.notify_type})

    if filter.status:
        search.update({"status": filter.status})

    sorted = DESCENDING if sort == "desc" else ASCENDING
    query = Notify.find(search, sort=[("created_at", sorted)])
    return await apaginate(query=query)
