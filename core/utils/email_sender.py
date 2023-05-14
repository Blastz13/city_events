import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE
from typing import List

from core.config import config

logger = logging.getLogger("app")


class EmailSender:
    SMTP_SERVER = config.SMTP_SERVER
    SMTP_PORT = config.SMTP_PORT
    SMTP_USERNAME = config.SMTP_USERNAME
    SMTP_PASSWORD = config.SMTP_PASSWORD

    def __init__(self):
        ...

    def send_email(self, subject, message, recipients):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            body = MIMEText(message)
            msg.attach(body)
            msg['To'] = self.join_recipients(recipients)

            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            server.starttls()
            server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
            server.sendmail(self.SMTP_USERNAME, recipients, msg.as_string())
            server.quit()
        except Exception as ex:
            logger.error(f"Error send email: {ex}")

    def join_recipients(self, recipients: str | List[str]) -> str:
        if isinstance(recipients, list):
            return COMMASPACE.join(recipients)
        return recipients
