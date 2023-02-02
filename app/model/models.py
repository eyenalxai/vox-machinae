from datetime import datetime

from sqlalchemy import BIGINT, TIMESTAMP, Boolean, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass  # noqa: WPS420, WPS604


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    username: Mapped[str | None] = mapped_column(
        String(32),  # noqa: WPS432 Found magic number
    )
    full_name: Mapped[str | None] = mapped_column(
        String(128),  # noqa: WPS432 Found magic number
    )

    tokens_used: Mapped[int] = mapped_column(Integer(), default=0)
