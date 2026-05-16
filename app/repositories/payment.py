import logging
from sqlalchemy import select

from app.db.models.payment import Payment
from app.repositories.base import BaseRepository


logger = logging.getLogger(__name__)


class PaymentRepository(BaseRepository[Payment]):
    model = Payment

    async def get_by_idempotency_key(
        self,
        provider: str,
        customer_id: str,
        idempotency_key: str,
    ) -> Payment | None:
        logger.debug(
            "querying payment by idempotency key",
            extra={"provider": provider, "customer_id": customer_id, "idempotency_key": idempotency_key},
        )

        query = select(Payment).where(
            Payment.provider == provider,
            Payment.customer_id == customer_id,
            Payment.idempotency_key == idempotency_key,
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_provider_reference(
        self,
        provider_reference: str,
    ) -> Payment | None:
        logger.debug("querying payment by provider reference", extra={"provider_reference": provider_reference})

        query = select(Payment).where(
            Payment.provider_reference == provider_reference
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_id_for_update(self,
                                   payment_id: int) -> Payment | None:
        query = (
            select(Payment)
            .where(Payment.id == payment_id)
            .with_for_update()
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()