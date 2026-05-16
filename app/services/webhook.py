import logging

from app.providers.factory import get_provider
from app.repositories.payment import PaymentRepository


logger = logging.getLogger(__name__)


class WebhookService:
    def __init__(self, db):
        self.db = db
        self.payment_repo = PaymentRepository(db)

    async def handle_payment_webhook(
        self,
        provider_name,
        payload: dict,
    ):
        logger.debug("handling payment webhook", extra={"provider": str(provider_name)})

        provider = get_provider(provider_name)

        try:
            normalized = provider.normalize_webhook_payload(payload)
        except Exception as exc:  # provider-specific parsing error
            logger.exception("failed to normalize webhook payload", exc_info=exc)
            raise

        provider_ref = normalized.get("provider_reference")
        logger.debug("normalized webhook payload", extra={"provider_reference": provider_ref})

        payment = await self.payment_repo.get_by_provider_reference(provider_ref)

        if not payment:
            logger.warning(
                "payment not found for webhook",
                extra={"provider": str(provider_name), "provider_reference": provider_ref},
            )
            return None

        await self.payment_repo.update(
            payment,
            {
                "status": normalized["status"],
                "raw_response": normalized["raw_response"],
            },
        )

        await self.db.commit()
        await self.db.refresh(payment)

        logger.info(
            "payment status updated from webhook",
            extra={"payment_id": payment.id, "status": payment.status},
        )

        return payment