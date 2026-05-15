from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.payment import Payment


class PaymentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict):

        payment = Payment(**data)

        self.db.add(payment)

        await self.db.commit()

        await self.db.refresh(payment)

        return payment

    async def get_by_id(self, payment_id: int):

        query = select(Payment).where(
            Payment.id == payment_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()