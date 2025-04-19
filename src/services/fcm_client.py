import logging
import random
from datetime import time
from typing import Any, Optional

from firebase_admin import credentials, initialize_app, messaging
from firebase_admin.exceptions import FirebaseError

from src.config import settings

logging.basicConfig(format="%(message)s", level=logging.INFO, force=True)
_log = logging.getLogger(__name__)


class FCMClient:
    """
    Handle Firebase Cloud Messaging (FCM) initialization and provides methods to send messages
    """

    _app = None
    _instance: Optional["FCMClient"] = None

    def __new__(cls, credentials_path: str) -> "FCMClient":
        if cls._instance is None:
            cls._instance = super(FCMClient, cls).__new__(cls)
        cls._instance._credentials_path = credentials_path
        return cls._instance

    def __init__(self, credentials_path: str):
        if self._app is None:
            self._initialize_app()

    def _initialize_app(self):
        cred = credentials.Certificate(cert=self._credentials_path)
        print("cred --> ", cred)
        self._app = initialize_app(credential=cred)

    @property
    def app(self):
        return self._app

    def _build_message(
            self,
            title: Any = None,
            body: Any = None,
            data: Any = None,
            image: Any = None,
            token: Any = None,
            **kwargs
    ) -> messaging.Message:
        return messaging.Message(
            notification=messaging.Notification(title=title, body=body, image=image),
            data=data,
            token=token,
            android=messaging.AndroidConfig(
                priority=settings.FCM_ANDROID_PRIORITY,
                ttl=settings.FCM_MESSAGING_TTL,
            ),
            apns=messaging.APNSConfig(
                headers={"apns-priority": settings.FCM_APNS_PRIORITY}
            ),
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(icon=image)
            ),
            **kwargs
        )

    def _handle_quota_exceeded(self, message: messaging.Message) -> Optional[str]:
        retries = 0
        while retries < settings.FCM_MAX_RETRIES:
            try:
                response = messaging.send(message)
                _log.info("Successfully sent message: ", response)
                return response
            except messaging.QuotaExceededError as exc:
                _log.error("Quota exceeded: ", exc)
                wait_time = (2 ** retries) + (random.randint(0, 1000) / 1000)
                time.sleep(wait_time)
                retries += 1
        return None

    def _handle_firebase_error(self, exc: FirebaseError):
        error_messages = {
            "INVALID_ARGUMENT": "Invalid message format: ",
            "UNREGISTERED": "Token is no longer valid: ",
            "SENDER_ID_MISMATCH": "Sender ID mismatch: "
        }
        message = error_messages.get(exc.code, "Failed to send message: ")
        _log.error(message, exc)

    def send_message(
            self,
            title: Any = None,
            body: Any = None,
            data: Any = None,
            image: Any = None,
            token: Any = None,
            **kwargs
    ) -> Optional[str]:
        message = self._build_message(title=title, body=body, data=data, image=image, token=token, **kwargs)

        try:
            response = messaging.send(message, dry_run=True)
            _log.info("Successfully sent message: ", response)
            return response
        except messaging.QuotaExceededError:
            return self._handle_quota_exceeded(message)
        except FirebaseError as exc:
            self._handle_firebase_error(exc)
        except Exception as exc:
            _log.error("Unexpected error ", exc)

        return None
