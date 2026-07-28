# This file simply imports methods from other files and connects to mail api,
# fetches emails and stores them in the database. It is an orchestration file

from sqlalchemy.orm import Session

from src.ingestion.providers.gmail import GmailProvider
from src.repositories.email_repository import EmailRepository
from src.repositories.sync_history_repository import SyncHistoryRepository
from src.repositories.sync_state_repository import SyncStateRepository


class SyncService:

    def __init__(self, db: Session):
        self.provider = GmailProvider()

        self.email_repository = EmailRepository(db)
        self.sync_history_repository = SyncHistoryRepository(db)
        self.sync_state_repository = SyncStateRepository(db)

    def sync(self):
        history = None

        try:
            # Create an audit record for this sync attempt
            history = self.sync_history_repository.create()

            # Authenticate with Gmail
            self.provider.authenticate()

            # Determine whether to perform a full sync or an incremental sync
            state = self.sync_state_repository.get("gmail")
            
            if state is None or state.last_history_id is None:
                # First sync - fetch the latest emails
                emails = self.provider.fetch_emails()
            
            else:
                # Incremental sync - fetch only emails that changed
                gmail_history = self.provider.get_history(
                    state.last_history_id
                )
                
                from pprint import pprint
                pprint(gmail_history)
            
                message_ids = self.provider.extract_message_ids(
                    gmail_history
                )
            
                emails = self.provider.fetch_emails_by_ids(
                    message_ids
                )

            stored = 0
            skipped = 0

            # Store only new emails
            for email in emails:
                existing = self.email_repository.get_by_message_id(
                    email.message_id
                )

                if existing:
                    skipped += 1
                    continue

                self.email_repository.create(email)
                stored += 1

            # Fetch the latest Gmail History ID
            history_id = self.provider.get_latest_history_id()

            # Update the sync checkpoint
            self.sync_state_repository.update_state(
                provider="gmail",
                history_id=history_id,
            )

            # Mark this sync as successful
            total_processed = stored + skipped

            self.sync_history_repository.mark_success(
                history=history,
                total_processed=total_processed,
                inserted=stored,
                skipped=skipped,
            )

            print(f"Stored : {stored}")
            print(f"Skipped: {skipped}")

        except Exception as e:
            if history is not None:
                self.sync_history_repository.mark_failed(history)

            raise