from sqlalchemy import ForeignKey, Numeric, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin


class Refund(Base, TimestampMixin):
    __tablename__ = "refunds"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    payment_id: Mapped[int] = mapped_column(
        ForeignKey("payments.id"),
        nullable=False,
        index=True,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    provider_reference: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    raw_response: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )