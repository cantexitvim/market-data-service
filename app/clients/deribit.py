import json
from decimal import Decimal
from typing import Literal

from app.core.settings import settings
from app.core.exceptions.client import ClientError
from app.clients.base import BaseClient


class DeribitClient(BaseClient):
    async def get_index_price(
        self, index_name: Literal["btc_usd", "eth_usd"]
    ) -> Decimal:
        url = f"{settings.deribit_url}/public/get_index_price"

        async with self.session.get(
            url,
            params={"index_name": index_name},
        ) as response:
            data = await response.json(
                loads=lambda text: json.loads(
                    text,
                    parse_float=Decimal,
                )
            )

            if response.status >= 400 or "error" in data:
                raise ClientError(status=response.status, response=data) from None

        return data["result"]["index_price"]
