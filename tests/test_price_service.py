from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.database.models import Price
from app.schemas.common import CollectionEnvelope, DateRange, PaginationParams
from app.schemas.prices import PriceSchema
from app.services.price import PriceService


async def test_get_last_price(mock_uow: MagicMock):
    db_price = Price(
        id=2,
        ticker="btc_usd",
        price=Decimal("67450.25"),
        timestamp=1792159226,
    )

    mock_uow.prices.get_last_price = AsyncMock(return_value=db_price)

    service = PriceService(uow=mock_uow)

    res = await service.get_last_price("btc_usd")

    assert isinstance(res, PriceSchema)
    assert res.ticker == db_price.ticker
    assert res.price == db_price.price
    assert res.timestamp == db_price.timestamp

    mock_uow.prices.get_last_price.assert_awaited_once_with("btc_usd")


async def test_get_prices(mock_uow: MagicMock):
    price_collection = CollectionEnvelope(
        items=[
            PriceSchema(
                id=2,
                ticker="btc_usd",
                price=Decimal("67450.25"),
                timestamp=1792159260,
            ),
            PriceSchema(
                id=1,
                ticker="btc_usd",
                price=Decimal("67453.87"),
                timestamp=1792159200,
            ),
        ],
        total=2,
        limit=10,
        offset=0,
    )

    mock_uow.prices.get_prices = AsyncMock(return_value=price_collection)

    service = PriceService(uow=mock_uow)

    res = await service.get_prices(
        ticker="btc_usd",
        sort_desc=False,
        date_range=DateRange(from_date="2026-10-16", to_date="2026-10-17"),
        pagination=PaginationParams(),
    )

    assert isinstance(res, CollectionEnvelope)
    assert res == price_collection

    mock_uow.prices.get_prices.assert_awaited_once_with(
        "btc_usd", False, from_time=1792108800, to_time=1792195200, limit=10, offset=0
    )


async def test_load_price(mock_uow: MagicMock, monkeypatch):
    mock_uow.prices.save = AsyncMock()

    deribit_client = AsyncMock()
    deribit_client.get_index_price = AsyncMock(return_value=Decimal("67450.25"))

    monkeypatch.setattr("app.services.price.time.time", lambda: 1792159226)

    service = PriceService(uow=mock_uow)

    res = await service.load_price(client=deribit_client, ticker="btc_usd")

    assert res is None

    mock_uow.prices.save.assert_awaited_once()

    saved_price = mock_uow.prices.save.await_args.args[0]

    assert isinstance(saved_price, Price)
    assert saved_price.ticker == "btc_usd"
    assert saved_price.price == Decimal("67450.25")
    assert saved_price.timestamp == 1792159226


async def test_load_price_client_fails(mock_uow: MagicMock):
    mock_uow.prices.save = AsyncMock()

    deribit_client = AsyncMock()
    deribit_client.get_index_price = AsyncMock(side_effect=RuntimeError("Deribit fail."))

    service = PriceService(uow=mock_uow)

    with pytest.raises(RuntimeError, match="Deribit fail."):
        await service.load_price(client=deribit_client, ticker="btc_usd")

    mock_uow.prices.save.assert_not_awaited()
