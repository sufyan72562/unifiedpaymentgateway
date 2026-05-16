from decimal import Decimal

from fastapi import HTTPException

from app.core.enums import PaymentStatus
from app.repositories.refund import RefundRepository
from app.repositories.payment import PaymentRepository


class RefundService:
    def __init__(self, db):
        self.db = db
        self.refund_repo = RefundRepository(db)
        self.payment_repo = PaymentRepository(db)
    
    async def refund_payment(self, payment_id: int, payload):
        payment = await self.payment_repo.get_by_id_for_update(
            payment_id
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found",
            )

        if payment.status in [
            PaymentStatus.FAILED.value,
            PaymentStatus.REFUNDED.value,
        ]:
            raise HTTPException(
                status_code=400,
                detail="Payment cannot be refunded",
            )

        total_refunded = (
            await self.refund_repo.get_total_refunded_amount(
                payment.id
            )
        )

        remaining_amount = (
            Decimal(payment.amount)
            - Decimal(total_refunded)
        )

        if payload.amount > remaining_amount:
            raise HTTPException(
                status_code=400,
                detail="Refund amount exceeds remaining balance",
            )

        refund = await self.refund_repo.create(
            {
                "payment_id": payment.id,
                "provider_reference": payment.provider_reference,
                "amount": payload.amount,
                "reason": payload.reason,
                "raw_response": {
                    "message": "Refund recorded",
                },
            }
        )

        updated_total_refunded = (
            Decimal(total_refunded)
            + payload.amount
        )

        if updated_total_refunded >= Decimal(payment.amount):
            new_status = PaymentStatus.REFUNDED.value
        else:
            new_status = (
                PaymentStatus.PARTIALLY_REFUNDED.value
            )

        await self.payment_repo.update(
            payment,
            {
                "status": new_status,
            },
        )

        await self.db.commit()

        await self.db.refresh(refund)

        return refund


