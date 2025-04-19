from fastapi import APIRouter, status, Body
from src.shared import select_provider
from src.config import settings
from src.schemas import EmailPayload

router = APIRouter(
    prefix="",
    tags=["NOTIFY"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

provider = select_provider(settings.NOTIFY_EMAIL_PROVIDER_CLASS)


@router.post("/send")
async def send(payload: EmailPayload = Body(...)):
    ret = await provider.send(**payload.model_dump())
    return ret
