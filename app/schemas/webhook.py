from pydantic import BaseModel


class ProviderAWebhookPayload(BaseModel):
    id: str
    state: str


class ProviderBWebhookPayload(BaseModel):
    transactionId: str
    paymentStatus: str