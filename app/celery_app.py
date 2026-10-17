from celery import Celery
from celery.schedules import crontab

from app.core.logger import setup_logger
from app.core.settings import settings

setup_logger()

celery_app = Celery(
    "market_data",
    broker=settings.redis_url,
    include=["app.tasks.prices"],
)

celery_app.conf.beat_schedule = {
    "collect-prices-every-minute": {
        "task": "app.tasks.prices.collect_prices",
        "schedule": crontab(minute="*"),
    },
}
