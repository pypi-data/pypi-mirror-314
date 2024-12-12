import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from base_lib.infra.db.mysql_database import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(60))

    profile_image_url: Mapped[str] = mapped_column(
        String(50), default="https://profileimageurl.com"
    )
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
