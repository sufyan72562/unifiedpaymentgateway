from app.providers.base import BasePaymentProvider
from app.schemas.payment import CreatePaymentRequest
from app.schemas.refund import RefundRequest


class ProviderB(BasePaymentProvider):

    async def create_payment(
        self,
        payload: CreatePaymentRequest,
    ) -> dict:
        return {
            "transactionId": "txn_987",
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
            "refundTransactionId": "refund_222",
            "refundStatus": "DONE",
            "transactionId": provider_reference,
            "refundAmount": str(payload.amount),
            "reason": payload.reason,
        }