from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector

from app.db.database import Base


class LegalChunkDB(Base):
    __tablename__ = "legal_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    chunk_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    document = Column(
        String,
        nullable=False,
    )

    article = Column(
        String,
        nullable=True,
        index=True,
    )

    recital = Column(
        String,
        nullable=True,
        index=True,
    )

    annex = Column(
        String,
        nullable=True,
        index=True,
    )

    heading = Column(
        String,
        nullable=True,
    )

    text = Column(
        Text,
        nullable=False,
    )

    source = Column(
        String,
        nullable=True,
    )

    version = Column(
        String,
        nullable=True,
    )

    embedding = Column(
        Vector(384),
        nullable=True,
    )