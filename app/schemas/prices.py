from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class PriceSchema(BaseModel):
    id: int
    ticker: str
    timestamp: int
    price: Decimal

    model_config = ConfigDict(from_attributes=True)
