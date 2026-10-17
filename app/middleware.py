import logging

from fastapi import FastAPI, Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


def register_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_exceptions(
        request: Request,
        call_next,
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            logger.error(
                "An unhandled error occurred while processing the HTTP request.",
                exc_info=exc,
                extra={
                    "http_status": 500,
                    "error_msg": str(exc),
                    "path": request.url.path,
                    "method": request.method,
                    "query_params": dict(request.query_params),
                    "client_ip": request.client.host if request.client else "unknown",
                    "user_agent": request.headers.get("user-agent", "unknown"),
                },
            )
            raise
