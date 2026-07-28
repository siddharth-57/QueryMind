#Encapsulate all database operations for SyncState in this repository
# this will read checkpoints and store them

from sqlalchemy.orm import Session

from src.database.models import SyncState
from datetime import datetime, UTC


class SyncStateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, provider: str) -> SyncState | None:
        return (
            self.db.query(SyncState)
            .filter(SyncState.provider == provider)
            .first()
        )

    def create(self, provider: str) -> SyncState:
        state = SyncState(provider=provider)

        self.db.add(state)
        self.db.commit()
        self.db.refresh(state)

        return state

    def update_state(
        self,
        provider: str,
        history_id: str,
    ) -> SyncState:
        state = self.get(provider)

        if state is None:
            state = self.create(provider)

        state.last_history_id = history_id
        state.last_synced_at = datetime.now(UTC)

        self.db.commit()
        self.db.refresh(state)

        return state