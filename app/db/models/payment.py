from sqlalchemy import String, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from decimal import Decimal

from app.db.base import Base, TimestampMixin


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "customer_id",
            "idempotency_key",
            name="uq_payment_idempotency",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)

    provider_reference: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    raw_response: Mapped[dict | None] = mapped_column(JSON, nullable=True)