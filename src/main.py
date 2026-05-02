from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.cache.redis_client import redis_client
from src.infrastructure.database.database import db_manager
from src.interfaces.api.routes.cars_router import router as car_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.initialize()
    await redis_client.initialize()
    yield
    await redis_client.close()
    await db_manager.close()

app = FastAPI(title="Default Redis Cache", lifespan=lifespan)

app.include_router(car_router)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        loop="uvloop",
        http="httptools"
    )
