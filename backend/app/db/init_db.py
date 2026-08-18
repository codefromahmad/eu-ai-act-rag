from sqlalchemy import text

from app.db.database import Base, engine
from app.db.models.analysis import AnalysisDB
from app.db.models.legal_chunk import LegalChunkDB


def init_db():

    with engine.begin() as connection:

        connection.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )
        )

    Base.metadata.create_all(
        bind=engine
    )