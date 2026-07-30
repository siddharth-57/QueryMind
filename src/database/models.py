import uuid
from datetime import datetime
from datetime import UTC

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import Boolean


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
    
    is_chunked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    
# we add this to provide the emailchunk table with the data of this table to be used as payload in vector db
    chunks: Mapped[list["EmailChunk"]] = relationship(
    back_populates="email",
    cascade="all, delete-orphan",
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
    
#Table to store chunks of emails
class EmailChunk(Base):
    __tablename__ = "email_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("emails.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    
    #This is needed because the data we want to store as payload for the embeddings is stored in the Emails table
    # and doing joins everytime we want to store data in vector db is more expensive
    email: Mapped["Email"] = relationship(
    back_populates="chunks",
    )