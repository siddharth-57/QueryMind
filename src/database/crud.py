from sqlalchemy.orm import Session

from src.database.models import Email


def get_email_by_message_id(
    db: Session,
    message_id: str,
) -> Email | None:
    return (
        db.query(Email)
        .filter(
            Email.outlook_message_id == message_id
        )
        .first()
    )


def create_email(
    db: Session,
    email: Email,
) -> Email:
    db.add(email)
    db.commit()
    db.refresh(email)

    return email