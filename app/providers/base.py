from abc import ABC, abstractmethod

from app.schemas.payment import CreatePaymentRequest
from app.schemas.refund import RefundRequest


class BasePaymentProvider(ABC):

    @abstractmethod
    async def create_payment(
        self,
        payload: CreatePaymentRequest,
    ) -> dict:
        pass

    @abstractmethod
    async def refund_payment(
        self,
        provider_reference: str,
        payload: RefundRequest,
    ) -> dict:
        pass

    @abstractmethod
    def normalize_payment_response(
        self,
        response: dict,
    ) -> dict:
        pass


    @abstractmethod
    def normalize_webhook_payload(self, payload: dict) -> dict:
        pass