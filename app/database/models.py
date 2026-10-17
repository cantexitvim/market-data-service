from sqlalchemy import func, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String, BigInteger, Numeric
from decimal import Decimal


class Base(DeclarativeBase):
    pass


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)

    ticker: Mapped[str] = mapped_column(String(10))
    timestamp: Mapped[int] = mapped_column(BigInteger)
    price: Mapped[Decimal] = mapped_column(Numeric(20, 8))

    __table_args__ = (Index("ix_prices_ticker_timestamp", "ticker", "timestamp"),)
