import asyncio
import logging

import aiohttp

from app.celery_app import celery_app
from app.clients.deribit import DeribitClient
from app.database.session import close_db, get_session_maker
from app.database.uow import UnitOfWork
from app.services.price import PriceService

logger = logging.getLogger(__name__)


@celery_app.task
def collect_prices():
    async def _collect_prices():
        try:
            uow = UnitOfWork(session_factory=get_session_maker())
            service = PriceService(uow=uow)

            async with aiohttp.ClientSession() as session:
                client = DeribitClient(session)

                await service.load_price(client, "btc_usd")
                await service.load_price(client, "eth_usd")
        finally:
            await close_db()

    try:
        asyncio.run(_collect_prices())
    except Exception as exc:
        logger.exception("Price collection task failed.", extra=exc.get("extra"))
        raise
