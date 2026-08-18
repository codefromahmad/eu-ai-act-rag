from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine


router = APIRouter(
    tags=["Health"],
)


@router.get("/health")
def health_check():
    """
    Liveness check.

    Confirms that the FastAPI application itself
    is running.
    """

    return {
        "status": "ok",
        "service": "eu-ai-act-rag-backend",
    }


@router.get("/ready")
def readiness_check():
    """
    Readiness check.

    Confirms that:
    - PostgreSQL is reachable.
    - pgvector is installed.
    """

    try:
        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

            vector_installed = (
                connection.execute(
                    text(
                        """
                        SELECT EXISTS (
                            SELECT 1
                            FROM pg_extension
                            WHERE extname = 'vector'
                        )
                        """
                    )
                )
                .scalar()
            )

        if not vector_installed:
            raise HTTPException(
                status_code=503,
                detail=(
                    "PostgreSQL is available, "
                    "but the pgvector extension "
                    "is not installed."
                ),
            )

        return {
            "status": "ready",
            "database": "connected",
            "pgvector": "available",
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail=(
                "The database is currently unavailable."
            ),
        )