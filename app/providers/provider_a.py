from app.providers.base import BasePaymentProvider
from app.schemas.payment import CreatePaymentRequest
from app.schemas.refund import RefundRequest


class ProviderA(BasePaymentProvider):

    async def create_payment(
        self,
        payload: CreatePaymentRequest,
    ) -> dict:

        return {
            "id": "pay_123",
            "state": "created",
            "amount": str(payload.amount),
            "currency": payload.currency,
        }

    async def refund_payment(
        self,
        provider_reference: str,
        payload: RefundRequest,
    ) -> dict:

        return {
            "refund_id": "refund_123",
            "status": "success",
        }