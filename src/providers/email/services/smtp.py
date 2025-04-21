import smtplib
import ssl
from contextlib import contextmanager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import lru_cache
from typing import Any, Optional, Union

from src.providers.base import Class, NotifyProvider
from src.providers.email.config import smtpconfig
from src.shared import logger, SMTPConnecttionError, EmailSentFailed


class SMTPProvider(NotifyProvider):

    def __init__(self):
        self.username = smtpconfig.SMTP_USERNAME
        self.password = smtpconfig.SMTP_PASSWORD
        self.server = smtpconfig.SMTP_SERVER
        self.port = smtpconfig.SMTP_PORT
        self.use_ssl = smtpconfig.SMTP_USE_SSL
        self.timeout = smtpconfig.SMTP_TIMEOUT
        self.debug = 1 if smtpconfig.SMTP_DEBUG else 0

    @contextmanager
    @lru_cache
    def connection(self):
        client = None
        try:
            if self.use_ssl:
                client = smtplib.SMTP_SSL(
                    host=self.server,
                    port=self.port,
                    local_hostname=self.server,
                    timeout=self.timeout,
                )
            else:
                client = smtplib.SMTP(
                    host=self.server,
                    port=self.port,
                    local_hostname=self.server,
                    timeout=self.timeout,
                )

            client.ehlo()
            client.set_debuglevel(debuglevel=self.debug)

            if not self.use_ssl:
                client.starttls(context=ssl.create_default_context())

            client.login(user=self.username, password=self.password)
            logger.info("SMTP connection established.")

            yield client
        except Exception as exc:
            logger.error(f"SMTP connection error: {str(exc)}")
            raise SMTPConnecttionError(f"Failed to establish SMTP connection: {str(exc)}")
        finally:
            if client:
                try:
                    client.quit()
                except Exception as e:
                    logger.warning(f"Error closing SMTP connection: {e}")

    async def send(self, model_klass: Optional[Class] = None, html_body: Optional[str] = None, **kwargs):
        """
        Send an email with optional HTML content
        """

        try:
            msg = MIMEMultipart("alternative")
            recipients = kwargs.get("recipients", [])

            if not recipients:
                raise ValueError("No recipients specified.")

            from_addr = kwargs.get("to")

            msg["From"] = from_addr
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = kwargs.get("subject")

            # Safer BCC management
            bcc_recipients = kwargs.get("hidden_copy", [])
            if bcc_recipients:
                msg["Bcc"] = ", ".join(bcc_recipients)

            # Message body
            msg.attach(MIMEText(_text=kwargs.get("body", ""), _subtype="plain"))
            if html_body:
                msg.attach(MIMEText(_text=html_body, _subtype="html"))

            with self.connection() as smtp:
                all_recipients = recipients + (list(bcc_recipients) if bcc_recipients else [])
                smtp.send_message(msg=msg, from_addr=from_addr, to_addrs=all_recipients)

                response = {
                    "status": "successful",
                    "recipients": len(all_recipients),
                }
                logger.info(f"Email sent to {len(recipients)} recipients")

        except Exception as exc:
            logger.error(f"Failed to send email: {exc}")
            raise EmailSentFailed(f"Email sending failed: {exc}")

        await model_klass(**kwargs).create() if model_klass else ""

        # Save to database in model class provided
        data = {"from_addr": from_addr, "to": ", ".join(recipients), "msg": msg}
        await model_klass(status="successful", notify_type="sms", data=data).create()

        return response

    async def status(self, notify_id: Union[Any, str]) -> Union[Any, Exception]:
        """
        Get the status of a send email.

        :param notify_id:
        :return:
        """
        pass

    async def find(self, query: dict = None, sort: str = None) -> list:
        pass

    async def find_one(self, sender_id: str) -> dict:
        pass
