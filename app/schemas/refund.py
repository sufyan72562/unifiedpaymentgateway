from decimal import Decimal

from pydantic import BaseModel, Field


class RefundRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    reason: str