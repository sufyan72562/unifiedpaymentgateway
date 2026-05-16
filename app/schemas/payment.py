from pydantic import BaseModel
from app.core.enums import PaymentProvider


class CreatePaymentRequest(BaseModel):
    amount: float
    currency: str
    customer_id: str
    provider: PaymentProvider


class PaymentResponse(BaseModel):
    id: int
    provider_reference: str | None = None
    amount: float
    currency: str
    status: str

    class Config:
        from_attributes = True