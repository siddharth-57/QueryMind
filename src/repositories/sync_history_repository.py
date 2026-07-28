from datetime import datetime

from sqlalchemy.orm import Session

from src.database.models import SyncHistory


class SyncHistoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self) -> SyncHistory:
        history = SyncHistory(
            started_at=datetime.utcnow(),
            status="RUNNING",
            total_processed=0,
            inserted=0,
            skipped=0,
            failed=0,
        )

        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)

        return history

    def mark_success(
        self,
        history: SyncHistory,
        total_processed: int,
        inserted: int,
        skipped: int,
    ) -> SyncHistory:

        history.finished_at = datetime.utcnow()
        history.status = "SUCCESS"
        history.total_processed = total_processed
        history.inserted = inserted
        history.skipped = skipped

        self.db.commit()
        self.db.refresh(history)

        return history

    def mark_failed(
        self,
        history: SyncHistory,
    ) -> SyncHistory:

        history.finished_at = datetime.utcnow()
        history.status = "FAILED"
        history.failed = 1

        self.db.commit()
        self.db.refresh(history)

        return history