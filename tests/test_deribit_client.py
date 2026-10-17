import pytest

from decimal import Decimal
from unittest.mock import AsyncMock, Mock, MagicMock

from app.clients.deribit import DeribitClient
from app.core.exceptions.client import ClientError
from app.core.settings import settings


async def test_get_index_price(mock_session: MagicMock, mock_response: Mock):
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={"result": {"index_price": Decimal("67450.25")}}
    )

    client = DeribitClient(session=mock_session)

    res = await client.get_index_price("btc_usd")

    assert res == Decimal("67450.25")

    mock_session.get.assert_called_once_with(
        f"{settings.deribit_url}/public/get_index_price",
        params={"index_name": "btc_usd"},
    )


async def test_get_index_price_fail(mock_session: MagicMock, mock_response: Mock):
    mock_response.status = 400
    mock_response.json = AsyncMock(return_value={"error": "Bad request"})

    client = DeribitClient(session=mock_session)

    with pytest.raises(ClientError):
        await client.get_index_price("btc_usd")
