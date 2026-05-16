from sqlalchemy import select

from app.db.models.payment import Payment
from app.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    model = Payment

    async def get_by_idempotency_key(
        self,
        provider: str,
        customer_id: str,
        idempotency_key: str,
    ) -> Payment | None:
        query = select(Payment).where(
            Payment.provider == provider,
            Payment.customer_id == customer_id,
            Payment.idempotency_key == idempotency_key,
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()