from sqlalchemy.orm import Session

from app.db.models.legal_chunk import LegalChunkDB
from app.models.compliance import ComplianceRequirement, LegalReference
from app.services.retrieval_service import RetrievalService


class RequirementRetrievalService:

    def __init__(self):
        self.retrieval = RetrievalService()

    def retrieve_for_requirement(
        self,
        db: Session,
        requirement: ComplianceRequirement,
        limit: int = 3,
    ) -> list[LegalReference]:

        references: list[LegalReference] = []

        # 1. Always fetch the primary legal Article directly
        primary = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.article
                == requirement.primary_article
            )
            .first()
        )

        if primary:
            references.append(
                LegalReference(
                    article=primary.article,
                    text=primary.text,
                )
            )

        # 2. Retrieve supplementary related Articles with RAG
        rag_results = self.retrieval.hybrid_search(
            db=db,
            query=requirement.query,
            limit=limit * 2,
        )

        # 3. Avoid duplicates
        existing_articles = {
            reference.article
            for reference in references
        }

        for result in rag_results:

            if result.article in existing_articles:
                continue

            references.append(
                LegalReference(
                    article=result.article,
                    text=result.text,
                )
            )

            existing_articles.add(result.article)

            if len(references) >= limit:
                break

        return references