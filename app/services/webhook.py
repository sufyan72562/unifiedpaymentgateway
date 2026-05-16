from app.providers.factory import get_provider
from app.repositories.payment import PaymentRepository


class WebhookService:
    def __init__(self, db):
        self.db = db
        self.payment_repo = PaymentRepository(db)

    async def handle_payment_webhook(
        self,
        provider_name,
        payload: dict,
    ):
        provider = get_provider(provider_name)

        normalized = provider.normalize_webhook_payload(payload)

        payment = await self.payment_repo.get_by_provider_reference(
            normalized["provider_reference"]
        )

        if not payment:
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

        return payment