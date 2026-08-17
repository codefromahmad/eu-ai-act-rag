from sqlalchemy.orm import Session

from app.db.models.legal_chunk import LegalChunkDB
from app.models.legal_document import LegalChunk


class LegalChunkRepository:

    @staticmethod
    def save_many(
        db: Session,
        chunks: list[LegalChunk],
        embeddings: list[list[float]],
    ) -> list[LegalChunkDB]:

        db_chunks = []

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):

            db_chunk = LegalChunkDB(
                chunk_id=chunk.chunk_id,
                document=chunk.document,
                article=chunk.article,
                recital=chunk.recital,
                annex=chunk.annex,
                heading=chunk.heading,
                text=chunk.text,
                source=chunk.source,
                version=chunk.version,
                embedding=embedding,
            )

            db.add(db_chunk)
            db_chunks.append(db_chunk)

        db.commit()

        return db_chunks