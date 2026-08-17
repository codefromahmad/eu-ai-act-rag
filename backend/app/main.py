from fastapi import FastAPI

from app.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.documents import router as documents_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-assisted preliminary EU AI Act compliance assessment system.",
    debug=settings.debug,
)


app.include_router(
    health_router,
    prefix="/api",
)

app.include_router(
    documents_router,
    prefix="/api",
)


@app.get("/")
async def root():
    return {
        "message": "EU AI Act RAG Compliance Analyzer",
        "version": settings.app_version,
    }