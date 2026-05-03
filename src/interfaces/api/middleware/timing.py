import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        if process_time > 0.5:
            logger.warning(
                f"SLOW REQUEST | {request.method} {request.url.path} | "
                f"{process_time:.3f}s | status={response.status_code}"
            )
        else:
            logger.debug(
                f"{request.method} {request.url.path} | "
                f"{process_time:.3f}s | status={response.status_code}"
            )
        return response
