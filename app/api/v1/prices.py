from fastapi import APIRouter, Depends

from app.services.price import PriceService
from app.schemas.common import (
    ResponseEnvelope,
    PaginationParams,
    DateRange,
    CollectionEnvelope,
)
from app.schemas.prices import PriceSchema
from typing import Literal

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get(
    "",
    name="get_prices",
    response_model=ResponseEnvelope[CollectionEnvelope[PriceSchema]],
)
async def get_prices(
    ticker: Literal["btc_usd", "eth_usd"],
    service: PriceService = Depends(),
    sort_desc: bool = False,
    date_range: DateRange = Depends(),
    pagination: PaginationParams = Depends(),
) -> ResponseEnvelope[CollectionEnvelope[PriceSchema]]:
    price_collection = await service.get_prices(
        ticker=ticker, sort_desc=sort_desc, date_range=date_range, pagination=pagination
    )

    return ResponseEnvelope(data=price_collection)


@router.get(
    "/last", name="get_last_price", response_model=ResponseEnvelope[PriceSchema]
)
async def get_last_price(
    ticker: Literal["btc_usd", "eth_usd"], service: PriceService = Depends()
) -> ResponseEnvelope[PriceSchema]:
    price = await service.get_last_price(ticker)

    return ResponseEnvelope(data=price)
