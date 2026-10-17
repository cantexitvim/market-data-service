from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse

from app.core.settings import settings
from app.api.v1 import v1_router
from app.core.logger import setup_logger
from app.database.session import close_db
from app.redis import redis_helper
from app.middleware import register_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_helper.init(settings.redis_url)

    yield

    await redis_helper.close()
    await close_db()


setup_logger()

app = FastAPI(
    title="market-data-service-api",
    docs_url="/docs" if settings.show_docs else None,
    redoc_url="/redoc" if settings.show_docs else None,
    openapi_url="/openapi.json" if settings.show_docs else None,
    debug=settings.debug,
)

register_middlewares(app)

app.include_router(v1_router)


@app.get("/favicon.ico")
def get_favicon() -> FileResponse:
    return FileResponse("favicon.ico")
