# Domain Model: Internal Email model
# This is the format in which we want to parse and collect data from an email

from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmailMessage:
    message_id: str
    conversation_id: str
    internet_message_id: str | None
    folder_name: str

    subject: str
    sender: str
    recipients: str
    body: str

    received_at: datetime
    has_attachments: bool