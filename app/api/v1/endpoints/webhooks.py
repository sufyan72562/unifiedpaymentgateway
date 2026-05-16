from fastapi import APIRouter, Depends, Header, HTTPException, Request
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.enums import PaymentProvider
from app.dependencies import get_db
from app.services.webhook import WebhookService

router = APIRouter(tags=["Webhooks"])

logger = logging.getLogger(__name__)


@router.post("/webhooks/{provider}")
async def payment_webhook(
    provider: PaymentProvider,
    request: Request,
    db: AsyncSession = Depends(get_db),
    webhook_secret: str = Header(..., alias="X-Webhook-Secret"),
):
    if webhook_secret != settings.WEBHOOK_SECRET:
        logger.warning("invalid webhook secret", extra={"provider": str(provider)})
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook secret",
        )

    payload = await request.json()
    logger.debug("received webhook", extra={"provider": str(provider), "payload_preview": str(payload)[:500]})

    service = WebhookService(db)

    payment = await service.handle_payment_webhook(
        provider_name=provider,
        payload=payload,
    )

    if not payment:
        logger.info("webhook referenced unknown payment", extra={"provider": str(provider)})
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    logger.info("webhook processed", extra={"payment_id": payment.id, "status": payment.status})

    return {
        "message": "Webhook processed successfully",
        "payment_id": payment.id,
        "status": payment.status,
    }