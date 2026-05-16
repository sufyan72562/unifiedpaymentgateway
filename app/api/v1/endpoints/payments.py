from fastapi import APIRouter, Depends, Header, HTTPException
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.payment import (
    CreatePaymentRequest,
    PaymentResponse,
)
from app.schemas.refund import RefundRequest
from app.services.payments import PaymentService

router = APIRouter(tags=["Payments"])

logger = logging.getLogger(__name__)


@router.post(
    "/payments",
    response_model=PaymentResponse,
    status_code=201,
)
async def create_payment(
    payload: CreatePaymentRequest,
    db: AsyncSession = Depends(get_db),
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    service = PaymentService(db)
    logger.debug("create_payment endpoint called", extra={"customer_id": payload.customer_id})

    return await service.create_payment(
        payload=payload,
        idempotency_key=idempotency_key,
    )


@router.get(
    "/payments/{payment_id}",
    response_model=PaymentResponse,
)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = PaymentService(db)
    payment = await service.get_payment(payment_id)

    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


@router.post(
    "/payments/{payment_id}/refund",
)
async def refund_payment(
    payment_id: int,
    payload: RefundRequest,
    db: AsyncSession = Depends(get_db),
):

    service = PaymentService(db)

    refund = await service.refund_payment(
        payment_id=payment_id,
        payload=payload,
    )

    return refund