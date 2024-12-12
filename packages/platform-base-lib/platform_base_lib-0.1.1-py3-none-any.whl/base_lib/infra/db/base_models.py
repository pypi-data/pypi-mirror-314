import uuid as uuid_pkg
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, String, text


class UUIDMixin:
    # Use CHAR(36) for UUIDs in MySQL
    uuid: uuid_pkg.UUID = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid_pkg.uuid4()),
        server_default=text("UUID()"),
    )


class TimestampMixin:
    # Use UTC-aware `datetime.now` with MySQL-compatible `CURRENT_TIMESTAMP`
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


class SoftDeleteMixin:
    # Add fields for soft delete functionality
    deleted_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False)
