import importlib
import time
import traceback
from contextlib import asynccontextmanager
from logging import getLogger
from uuid import uuid4

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from beamlit.common.settings import get_settings, init

main_agent = None


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger = getLogger(__name__)
        response = await call_next(request)
        process_time = response.headers.get("X-Process-Time")
        rid_header = response.headers.get("X-Request-Id")
        request_id = rid_header or response.headers.get("X-Beamlit-Request-Id")
        logger.info(f"{request.method} {request.url.path} {response.status_code} {process_time}ms rid={request_id}")
        return response


class AddProcessTimeHeader(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time"] = f"{process_time:.2f}"
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        is_main = __name__ == "main"
        if not is_main:
            init()

        logger = getLogger(__name__)
        settings = get_settings()

        # Import the agent
        global main_agent
        main_agent = importlib.import_module(".".join(settings.agent_module.split(".")[0:-1]))
        # Log the server is running
        if is_main:
            logger.info(f"Server running on http://{settings.host}:{settings.port}")
        yield
    except Exception as e:
        logger = getLogger(__name__)
        logger.error(f"Error initializing agent: {e}", exc_info=True)
        raise e


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="x-beamlit-request-id",
    generator=lambda: str(uuid4()),
)
app.add_middleware(AddProcessTimeHeader)
app.add_middleware(AccessLogMiddleware)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/")
async def root(request: Request):
    settings = get_settings()
    logger = getLogger(__name__)
    try:
        func = getattr(main_agent, settings.agent_module.split(".")[-1])
        body = await request.json()
        response = await func(body)
        if isinstance(response, Response):
            return response
        if type(response) is str:
            return Response(
                content=response,
                headers={"Content-Type": "text/plain"},
                media_type="text/plain",
                status_code=200,
            )
        return JSONResponse(status_code=200, content=response)
    except ValueError as e:
        content = {"error": str(e)}
        if settings.environment == "development":
            content["traceback"] = str(traceback.format_exc())
        logger.error(f"{content}")
        return JSONResponse(status_code=400, content=content)
    except Exception as e:
        content = {"error": f"Internal server error, {e}"}
        if settings.environment == "development":
            content["traceback"] = str(traceback.format_exc())
        return JSONResponse(status_code=500, content=content)


def main():
    settings = init()
    uvicorn.run(
        f"{__name__}:app",
        host=settings.host,
        port=settings.port,
        log_level="critical",
        reload=settings.environment != "production",
    )


if __name__ == "__main__":
    main()
