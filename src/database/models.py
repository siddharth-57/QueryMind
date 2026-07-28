from sqlalchemy.orm import DeclarativeBase
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Every table in this project will inherit from this base.
# This is how SQLAlchemy will know which classes represent database tables.
class Base(DeclarativeBase):
    pass


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    outlook_message_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    conversation_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    internet_message_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    subject: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sender: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    recipients: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    folder_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    has_attachments: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

# Every sync ever performed. useful for Audit Log.
class SyncHistory(Base):
    __tablename__ = "sync_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    total_processed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    inserted: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    skipped: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    failed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    
# Current synchronization checkpoint
class SyncState(Base):
    __tablename__ = "sync_state"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    last_history_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )