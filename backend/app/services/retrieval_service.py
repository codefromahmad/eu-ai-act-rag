from sqlalchemy.orm import Session

from app.db.models.legal_chunk import LegalChunkDB
from app.services.embedding_service import EmbeddingService


class RetrievalService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        

    def semantic_search(
        self,
        db: Session,
        query: str,
        limit: int = 5,
    ):

        query_embedding = (
            self.embedding_service.embed_text(
                query
            )
        )

        results = (
            db.query(LegalChunkDB)
            .order_by(
                LegalChunkDB.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
            .all()
        )

        return results

    def keyword_search(
        self,
        db: Session,
        query: str,
        limit: int = 5,
    ):
        results = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.text.ilike(
                    f"%{query}%"
                )
            )
            .limit(limit)
            .all()
        )

        return results

    def hybrid_search(
        self,
        db: Session,
        query: str,
        limit: int = 5,
    ):
        semantic_results = self.semantic_search(
            db=db,
            query=query,
            limit=limit * 2,
        )

        keyword_results = self.keyword_search(
            db=db,
            query=query,
            limit=limit * 2,
        )

        scores = {}
        chunks = {}

        k = 60

        for rank, chunk in enumerate(
            semantic_results,
            start=1,
        ):
            chunks[chunk.id] = chunk

            scores[chunk.id] = (
                scores.get(chunk.id, 0)
                + 1 / (k + rank)
            )

        for rank, chunk in enumerate(
            keyword_results,
            start=1,
        ):
            chunks[chunk.id] = chunk

            scores[chunk.id] = (
                scores.get(chunk.id, 0)
                + 1 / (k + rank)
            )

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )

        return [
            chunks[chunk_id]
            for chunk_id in ranked_ids[:limit]
        ]