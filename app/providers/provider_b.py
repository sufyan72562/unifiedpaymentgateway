from decimal import Decimal

from app.core.enums import PaymentStatus
from app.providers.base import BasePaymentProvider


class ProviderB(BasePaymentProvider):

    async def create_payment(
        self,
        payload,
    ) -> dict:

        return {
            "transactionId": "txn_B_987",
            "paymentStatus": "INITIATED",
            "totalAmount": "100.50",
            "currencyCode": "SAR",
        }

    async def refund_payment(
        self,
        provider_reference,
        payload,
    ) -> dict:

        return {
            "refund_id": "refund_222",
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