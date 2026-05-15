from pydantic import BaseModel


class RefundRequest(BaseModel):
    amount: float
    reason: str