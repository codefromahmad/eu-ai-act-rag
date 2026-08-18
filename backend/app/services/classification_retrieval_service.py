from sqlalchemy.orm import Session

from app.db.models.legal_chunk import LegalChunkDB
from app.models.compliance import LegalReference
from app.services.retrieval_service import RetrievalService


class ClassificationRetrievalService:

    def __init__(self):
        self.retrieval = RetrievalService()

    def retrieve(
        self,
        db: Session,
        query: str,
        limit: int = 5,
    ) -> list[LegalReference]:

        references: list[LegalReference] = []
        seen: set[str] = set()

        # --------------------------------------------------
        # 1. Always include Article 6
        #    High-risk classification rules
        # --------------------------------------------------

        article_6 = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.article == "Article 6"
            )
            .first()
        )

        if article_6:
            references.append(
                LegalReference(
                    article="Article 6",
                    text=article_6.text,
                )
            )

            seen.add("Article 6")

        # --------------------------------------------------
        # 2. Always include Annex III
        #    High-risk use cases
        # --------------------------------------------------

        annex_iii = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.annex == "Annex III"
            )
            .first()
        )

        if annex_iii:
            references.append(
                LegalReference(
                    article="Annex III",
                    text=annex_iii.text,
                )
            )

            seen.add("Annex III")

        # --------------------------------------------------
        # 3. Add supplementary hybrid retrieval results
        # --------------------------------------------------

        results = self.retrieval.hybrid_search(
            db=db,
            query=query,
            limit=limit * 2,
        )

        for result in results:

            reference_name = (
                result.article
                if result.article
                else result.annex
            )

            if not reference_name:
                continue

            if reference_name in seen:
                continue

            references.append(
                LegalReference(
                    article=reference_name,
                    text=result.text,
                )
            )

            seen.add(reference_name)

            if len(references) >= limit:
                break

        return references