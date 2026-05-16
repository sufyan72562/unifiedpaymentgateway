import logging
from sqlalchemy.exc import IntegrityError

from app.core.enums import PaymentStatus
from app.db.models.payment import Payment
from app.providers.factory import get_provider
from app.repositories.payment import PaymentRepository


logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, db):
        self.db = db
        self.payment_repo = PaymentRepository(db)

    async def create_payment(
        self,
        payload,
        idempotency_key: str,
    ):
        logger.debug(
            "create_payment called",
            extra={"provider": str(payload.provider), "customer_id": payload.customer_id},
        )
        existing_payment = await self.payment_repo.get_by_idempotency_key(
            provider=payload.provider.value,
            customer_id=payload.customer_id,
            idempotency_key=idempotency_key,
        )

        if existing_payment:
            return existing_payment

        try:
            payment = await self.payment_repo.create(
                {
                    "provider": payload.provider.value,
                    "customer_id": payload.customer_id,
                    "idempotency_key": idempotency_key,
                    "provider_reference": None,
                    "amount": payload.amount,
                    "currency": payload.currency,
                    "status": PaymentStatus.PROCESSING.value,
                    "raw_response": None,
                }
            )

            await self.db.commit()
            await self.db.refresh(payment)

        except IntegrityError:
            await self.db.rollback()

            logger.info("integrity error on create, returning existing payment")

            return await self.payment_repo.get_by_idempotency_key(
                provider=payload.provider.value,
                customer_id=payload.customer_id,
                idempotency_key=idempotency_key,
            )

        provider = get_provider(payload.provider)

        try:
            raw_response = await provider.create_payment(
                payload=payload,
                idempotency_key=idempotency_key,
            )

            normalized = provider.normalize_payment_response(raw_response)

            await self.payment_repo.update(
                payment,
                {
                    "provider_reference": normalized["provider_reference"],
                    "amount": normalized["amount"],
                    "currency": normalized["currency"],
                    "status": normalized["status"],
                    "raw_response": normalized["raw_response"],
                },
            )

            await self.db.commit()
            await self.db.refresh(payment)

            logger.info("payment created and updated", extra={"payment_id": payment.id, "status": payment.status})
            return payment

        except Exception:
            await self.db.rollback()

            payment.status = PaymentStatus.FAILED.value
            await self.db.commit()
            await self.db.refresh(payment)

            logger.exception("payment processing failed, marked as failed", extra={"payment_id": payment.id})

            raise

    async def get_payment(self, payment_id: int) -> Payment | None:
        logger.debug("get_payment called", extra={"payment_id": payment_id})
        return await self.payment_repo.get_by_id(payment_id)
