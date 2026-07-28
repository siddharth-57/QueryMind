# Instead of inserting directly from GmailProvider, we'll use a repository.
# GmailProvider will only communicate with Gmail.
# Database operations will be in the repository layer. This separation makes it much easier to test and maintain.

from sqlalchemy.orm import Session

from src.database.models import Email
from src.models.email_message import EmailMessage


class EmailRepository:
    def __init__(self, db: Session):
        self.db = db
        
# mapping from our internal EmailMessage dataclass to the SQLAlchemy Email model.
    
    def create(self, email: EmailMessage) -> Email:
        db_email = Email(
            outlook_message_id=email.message_id,

            conversation_id=email.conversation_id,
            internet_message_id=email.internet_message_id,
            folder_name=email.folder_name,

            subject=email.subject,
            sender=email.sender,
            recipients=email.recipients,

            body=email.body,
            received_at=email.received_at,
            has_attachments=email.has_attachments,
        )

        self.db.add(db_email)
        self.db.commit()
        self.db.refresh(db_email)

        return db_email
    
# This helper function helps us prevent duplicates in the database
    def get_by_message_id(self, message_id: str):
        return (
            self.db.query(Email)
            .filter(
                Email.outlook_message_id == message_id
            )
            .first()
        )
        
        

    def get_unchunked_emails(self) -> list[Email]:
        return (
            self.db.query(Email)
            .filter(Email.is_chunked.is_(False))
            .all()
        )
    
    
    
    def mark_as_chunked(self, email_id: int) -> None:
        email = (
            self.db.query(Email)
            .filter(Email.id == email_id)
            .first()
        )

        if email is None:
            return

        email.is_chunked = True
        self.db.commit()