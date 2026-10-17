import time
from datetime import UTC, date, datetime
from datetime import time as dt_time

from fastapi import Depends

from app.clients.base import BaseClient
from app.database.models import Price
from app.database.uow import UnitOfWork
from app.schemas.common import CollectionEnvelope, DateRange, PaginationParams
from app.schemas.prices import PriceSchema


class PriceService:
    def __init__(self, uow: UnitOfWork = Depends()):
        self.uow = uow

    async def get_prices(
        self,
        ticker: str,
        sort_desc: bool,
        date_range: DateRange,
        pagination: PaginationParams,
    ) -> CollectionEnvelope[PriceSchema]:
        from_time = self._date_to_timestamp(date_range.from_date)
        to_time = self._date_to_timestamp(date_range.to_date)

        async with self.uow:
            price_collection = await self.uow.prices.get_prices(
                ticker,
                sort_desc,
                from_time=from_time,
                to_time=to_time,
                **pagination.model_dump(),
            )

            return price_collection

    async def get_last_price(self, ticker: str) -> PriceSchema:
        async with self.uow:
            db_price = await self.uow.prices.get_last_price(ticker)

            price = PriceSchema.model_validate(db_price)

            return price

    async def load_price(self, client: BaseClient, ticker: str) -> None:
        index_price = await client.get_index_price(ticker)

        db_price = Price(
            ticker=ticker,
            price=index_price,
            timestamp=int(time.time()),
        )

        async with self.uow:
            await self.uow.prices.save(db_price)

    def _date_to_timestamp(self, dt: date | None) -> int | None:
        if dt is not None:
            timestamp = int(datetime.combine(dt, dt_time.min, tzinfo=UTC).timestamp())

            return timestamp
