from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode, urljoin

import httpx
from anyio import sleep_forever

from src.providers.base import Class, NotifyProvider
from src.providers.sms.config import smsconfig
from src.shared import logger, SMSException


class SMSProvider(NotifyProvider):

    def __init__(self):
        self.headers: Dict[str, Any] = {}
        self.params: Dict[str, Any] = {}
        self.type = smsconfig.SMS_TYPE
        self.url = smsconfig.SMS_BASE_URL
        self.sender = smsconfig.SMS_SENDER

    async def send(self, model_klass: Optional[Class] = None, **kwargs) -> Dict[str, Any]:

        # Validate required parameters
        recipient = kwargs.get("recipient")
        message = kwargs.get("message")

        if not recipient or not message:
            raise ValueError("Both recipient and message are required.")

        try:
            # Prepare request parameters
            self.params.update({
                "from": self.sender, "to": kwargs.get("recipient"),
                "type": self.type, "message": kwargs.get("message"),
                "dlr": 1
            })

            self.headers.update({
                "APIKEY": smsconfig.SMS_API_KEY,
                "CLIENTID": smsconfig.SMS_CLIENT_ID,
            })

            # Build the full URL
            url = urljoin(self.url, "?" + urlencode(self.params))
            logger.debug(f"Sending SMS to {recipient} via {url}")

            async with httpx.AsyncClient(follow_redirects=True, timeout=httpx.Timeout(30.0)) as client:
                response = await client.post(url=url, headers=self.headers)

                try:
                    response.raise_for_status()

                    json_resp = response.json()
                    logger.debug(f"SMS API response: {json_resp}")
                except ValueError as json_err:
                    # Handle empty or invalid JSON response
                    logger.warning(f"Invalid JSON response: {response.text}")

                    return {
                        "status": "success" if response.status_code == 200 else "unknown",
                        "message": "SMS sent but no valid response received",
                        "raw_response": response.text
                    }

                # Save to database in model class provided
                data = {"message_id": json_resp["messageId"], "to": json_resp["to"], "msg": json_resp["message"]}
                await model_klass(status="successful", notify_type="sms", data=data).create()

                return json_resp

        except httpx.HTTPStatusError as exc:
            logger.error(f"HTTP status  error: {exc}")
            raise SMSException(f"HTTP status error '{exc}' while sending SMS") from exc
        except httpx.HTTPError as exc:
            logger.error(f"HTTP error: {exc}")
            raise SMSException(f"HTTP error '{exc}' while sending SMS") from exc

    async def status(self, notify_id: Union[Any, str]) -> Union[Any, Exception]:
        pass

    async def find(self, query: dict = None, sort: str = None) -> list:
        pass

    async def find_one(self, sender_id: str) -> dict:
        pass
