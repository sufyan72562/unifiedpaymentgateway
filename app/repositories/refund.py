from sqlalchemy import func, select

from app.db.models.refund import Refund
from app.repositories.base import BaseRepository



class RefundRepository(BaseRepository[Refund]):
    model = Refund

    async def get_total_refunded_amount(
        self,
        payment_id: int,
    ):
        query = select(
            func.coalesce(
                func.sum(Refund.amount),
                0,
            )
        ).where(
            Refund.payment_id == payment_id
        )

        result = await self.db.execute(query)

        return result.scalar()