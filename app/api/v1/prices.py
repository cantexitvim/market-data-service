from typing import Literal

from fastapi import APIRouter, Depends

from app.schemas.common import (
    CollectionEnvelope,
    DateRange,
    PaginationParams,
    ResponseEnvelope,
)
from app.schemas.prices import PriceSchema
from app.services.price import PriceService

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get(
    "",
    name="get_prices",
    summary="Получить историю цен",
    description=(
        "Возвращает историю ценового индекса для указанного тикера. "
        "Поддерживает фильтрацию по диапазону дат, сортировку по времени "
        "и пагинацию результатов. "
        "Временной диапазон необходимо указывать в формате ISO. Например: 2026-10-17"
    ),
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
    "/last",
    name="get_last_price",
    summary="Получить последнюю цену",
    description=(
        "Возвращает последнюю сохранённую цену для указанного тикера. "
        "Если для тикера нет сохранённых данных, результат зависит "
        "от обработки этого случая в сервисном слое."
    ),
    response_model=ResponseEnvelope[PriceSchema],
)
async def get_last_price(
    ticker: Literal["btc_usd", "eth_usd"], service: PriceService = Depends()
) -> ResponseEnvelope[PriceSchema]:
    price = await service.get_last_price(ticker)

    return ResponseEnvelope(data=price)
