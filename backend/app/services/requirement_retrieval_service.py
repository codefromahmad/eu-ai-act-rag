from sqlalchemy.orm import Session

from app.models.compliance import LegalReference
from app.services.retrieval_service import RetrievalService


class RequirementRetrievalService:

    def __init__(self):
        self.retrieval = RetrievalService()

    def retrieve_legal_references(
        self,
        db: Session,
        query: str,
        limit: int = 3,
    ) -> list[LegalReference]:

        results = self.retrieval.hybrid_search(
            db=db,
            query=query,
            limit=limit,
        )

        return [
            LegalReference(
                article=result.article,
                text=result.text,
            )
            for result in results
        ]