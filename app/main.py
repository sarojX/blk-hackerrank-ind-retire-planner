from fastapi import FastAPI

from app.core.config import settings
from app.routers.performance import router as performance_router
from app.routers.returns import router as returns_router
from app.routers.transactions import router as transactions_router

app = FastAPI(title=settings.app_name, version=settings.version)
app.include_router(transactions_router)
app.include_router(returns_router)
app.include_router(performance_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
