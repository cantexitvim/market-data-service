from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PriceSchema(BaseModel):
    id: int
    ticker: str
    timestamp: int
    price: Decimal

    model_config = ConfigDict(from_attributes=True)
