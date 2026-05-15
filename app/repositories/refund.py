from sqlalchemy import select

from app.db.models.refund import Refund
from app.repositories.base import BaseRepository


class RefundRepository(BaseRepository[Refund]):
    model = Refund

    async def get_by_payment_id(
        self,
        payment_id: int,
    ) -> list[Refund]:
        query = select(Refund).where(
            Refund.payment_id == payment_id
        )

        result = await self.db.execute(query)

        return list(result.scalars().all())