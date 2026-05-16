from decimal import Decimal
from app.schemas.payment import CreatePaymentRequest
from app.schemas.refund import RefundRequest
from app.core.enums import PaymentStatus
from app.providers.base import BasePaymentProvider


class ProviderA(BasePaymentProvider):

    async def create_payment(
        self,
        payload: CreatePaymentRequest,
    ) -> dict:

        return {
            "id": "pay_A_123",
            "state": "created",
            "amount": 10050,
            "currency": "SAR",
        }

    async def refund_payment(
        self,
        provider_reference: str,
        payload: RefundRequest,
    ) -> dict:

        return {
            "refund_id": "refund_123",
        }

    def normalize_payment_response(
        self,
        response: dict,
    ) -> dict:

        return {
            "provider_reference": response["id"],
            "amount": Decimal(response["amount"]) / Decimal("100"),
            "currency": response["currency"],
            "status": PaymentStatus.PENDING.value,
            "raw_response": response,
        }
    
    def normalize_webhook_payload(self, payload: dict) -> dict:
        status_map = {
            "created": PaymentStatus.PENDING.value,
            "paid": PaymentStatus.SUCCESS.value,
            "failed": PaymentStatus.FAILED.value,
            "refunded": PaymentStatus.REFUNDED.value,
        }

        return {
            "provider_reference": payload["id"],
            "status": status_map.get(
                payload["state"],
                PaymentStatus.PENDING.value,
            ),
            "raw_response": payload,
        }