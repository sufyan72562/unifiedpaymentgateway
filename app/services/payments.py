from app.providers.factory import get_provider
from app.repositories.payment import PaymentRepository
from app.repositories.refund import RefundRepository
from app.utils.mapper import normalize_provider_response


class PaymentService:

    def __init__(self, db):
        self.payment_repo = PaymentRepository(db)
        self.refund_repo = RefundRepository(db)

    async def create_payment(
        self,
        payload,
    ):

        provider = get_provider(
            payload.provider,
        )

        provider_response = await provider.create_payment(
            payload,
        )

        normalized = normalize_provider_response(
            payload.provider.value,
            provider_response,
        )

        normalized["provider"] = payload.provider.value

        payment = await self.payment_repo.create(
            normalized,
        )

        return payment

    async def get_payment(
        self,
        payment_id: int,
    ):

        return await self.payment_repo.get_by_id(
            payment_id,
        )

    async def refund_payment(
        self,
        payment_id: int,
        payload,
    ):

        payment = await self.payment_repo.get_by_id(
            payment_id,
        )

        if not payment:
            raise ValueError("Payment not found")

        provider = get_provider(
            payment.provider,
        )

        provider_response = await provider.refund_payment(
            provider_reference=payment.provider_reference,
            payload=payload,
        )

        refund = await self.refund_repo.create(
            {
                "payment_id": payment.id,
                "amount": payload.amount,
                "reason": payload.reason,
                "provider_reference": provider_response.get(
                    "refund_id"
                )
                or provider_response.get(
                    "refundTransactionId"
                ),
                "raw_response": provider_response,
            }
        )

        return refund