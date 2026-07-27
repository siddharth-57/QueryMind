# This file simply imports methods from other files and connects to mail api, fetches emails and stores in database

from sqlalchemy.orm import Session

from src.ingestion.providers.gmail import GmailProvider
from src.repositories.email_repository import EmailRepository


class SyncService:

    def __init__(self, db: Session):
        self.provider = GmailProvider()
        self.repository = EmailRepository(db)

    def sync(self):

        self.provider.authenticate()

        emails = self.provider.fetch_emails()

        stored = 0
        skipped = 0

        for email in emails:

            existing = self.repository.get_by_message_id(
                email.message_id
            )

        # Prevents duplicates from being stored in the database
            if existing:
                skipped += 1
                continue

            self.repository.create(email)
            stored += 1

        print(f"Stored : {stored}")
        print(f"Skipped: {skipped}")