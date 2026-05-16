from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.enums import PaymentProvider
from app.dependencies import get_db
from app.services.webhook import WebhookService

router = APIRouter(tags=["Webhooks"])


@router.post("/webhooks/{provider}")
async def payment_webhook(
    provider: PaymentProvider,
    request: Request,
    db: AsyncSession = Depends(get_db),
    webhook_secret: str = Header(..., alias="X-Webhook-Secret"),
):
    if webhook_secret != settings.WEBHOOK_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook secret",
        )

    payload = await request.json()

    service = WebhookService(db)

    payment = await service.handle_payment_webhook(
        provider_name=provider,
        payload=payload,
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    return {
        "message": "Webhook processed successfully",
        "payment_id": payment.id,
        "status": payment.status,
    }