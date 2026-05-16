from decimal import Decimal
from uuid import uuid4
from app.schemas.payment import CreatePaymentRequest
from app.schemas.refund import RefundRequest
from app.core.enums import PaymentStatus
from app.providers.base import BasePaymentProvider


class ProviderB(BasePaymentProvider):

    async def create_payment(
        self,
        payload: CreatePaymentRequest,
        idempotency_key: str | None = None,
    ) -> dict:
        return {
            "transactionId": f"txn_B_{uuid4().hex[:10]}",
            "paymentStatus": "INITIATED",
            "totalAmount": str(payload.amount),
            "currencyCode": payload.currency,
        }

    async def refund_payment(
        self,
        provider_reference: str,
        payload: RefundRequest,
    ) -> dict:
        return {
            "refundTransactionId": f"refund_B_{uuid4().hex[:10]}",
        }

    def normalize_payment_response(
        self,
        response: dict,
    ) -> dict:
        return {
            "provider_reference": response["transactionId"],
            "amount": Decimal(response["totalAmount"]),
            "currency": response["currencyCode"],
            "status": PaymentStatus.PENDING.value,
            "raw_response": response,
        }