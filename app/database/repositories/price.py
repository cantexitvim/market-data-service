from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.models import Price
from app.schemas.prices import PriceSchema
from app.schemas.common import CollectionEnvelope


class PriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_prices(
        self,
        ticker: str,
        sort_desc: bool = False,
        from_time: int | None = None,
        to_time: int | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> CollectionEnvelope[PriceSchema]:
        query = select(
            Price.id,
            Price.ticker,
            Price.price,
            Price.timestamp,
        ).where(Price.ticker == ticker)

        if from_time is not None:
            query = query.where(Price.timestamp >= from_time)

        if to_time is not None:
            query = query.where(Price.timestamp < to_time)

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query) or 0

        if sort_desc:
            query = query.order_by(Price.timestamp.desc())
        else:
            query = query.order_by(Price.timestamp.asc())

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)

        rows = result.mappings().all()

        prices = [PriceSchema.model_validate(row) for row in rows]

        collection = CollectionEnvelope(
            items=prices,
            total=total,
            limit=limit,
            offset=offset,
        )

        return collection

    async def get_last_price(self, ticker: str) -> Price:
        query = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(Price.timestamp.desc())
            .limit(1)
        )

        db_price = await self.session.scalar(query)

        return db_price

    async def save(self, price: Price) -> None:
        self.session.add(price)

        await self.session.flush()
