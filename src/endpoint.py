from fastapi import APIRouter, status

router = APIRouter(
    prefix="",
    tags=["NOTIFY"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/send", summary="Send a message", status_code=status.HTTP_201_CREATED)
async def send_message():
    return {"message": "Message sent successfully"}


@router.get("/read", summary="Get all messages", status_code=status.HTTP_200_OK)
async def get_messages():
    return {"message": "Messages retrieved successfully"}
