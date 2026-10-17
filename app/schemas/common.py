from datetime import date
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class ResponseEnvelope(BaseModel, Generic[T]):
    data: T


class CollectionEnvelope(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int | None = None
    offset: int | None = None


class PaginationParams(BaseModel):
    limit: int = Query(default=10, ge=1, le=100)
    offset: int = Query(default=0, ge=0)


class DateRange(BaseModel):
    from_date: date | None = None
    to_date: date | None = None
