from fastapi import APIRouter, status

router = APIRouter(
    prefix="",
    tags=["NOTIFY"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
