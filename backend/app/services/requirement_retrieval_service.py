import re

from sqlalchemy.orm import Session

from app.db.models.legal_chunk import LegalChunkDB
from app.models.compliance import (
    ComplianceRequirement,
    LegalReference,
)
from app.services.retrieval_service import RetrievalService


class RequirementRetrievalService:

    ANNEX_REFERENCE_PATTERN = re.compile(
        r"\bAnnex\s+([IVXLCDM]+)\b",
        re.IGNORECASE,
    )

    def __init__(self):
        self.retrieval = RetrievalService()

    def _extract_annex_references(
        self,
        text: str,
    ) -> list[str]:

        matches = self.ANNEX_REFERENCE_PATTERN.findall(
            text
        )

        references = []

        for match in matches:
            annex = f"Annex {match.upper()}"

            if annex not in references:
                references.append(annex)

        return references

    def retrieve_for_requirement(
        self,
        db: Session,
        requirement: ComplianceRequirement,
        limit: int = 3,
    ) -> list[LegalReference]:

        references: list[LegalReference] = []
        existing_references: set[str] = set()

        # 1. Fetch primary Article directly
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

            existing_references.add(
                primary.article
            )

            # 2. Detect Annex references inside the primary Article
            referenced_annexes = (
                self._extract_annex_references(
                    primary.text
                )
            )

            # 3. Fetch referenced Annexes directly
            for annex_name in referenced_annexes:

                annex_chunk = (
                    db.query(LegalChunkDB)
                    .filter(
                        LegalChunkDB.annex
                        == annex_name
                    )
                    .first()
                )

                if annex_chunk:

                    references.append(
                        LegalReference(
                            article=annex_chunk.annex,
                            text=annex_chunk.text,
                        )
                    )

                    existing_references.add(
                        annex_chunk.annex
                    )

                    if len(references) >= limit:
                        return references

        # 4. Add supplementary hybrid RAG results
        rag_results = self.retrieval.hybrid_search(
            db=db,
            query=requirement.query,
            limit=limit * 2,
        )

        for result in rag_results:

            reference_name = (
                result.article
                if result.article
                else result.annex
            )

            if not reference_name:
                continue

            if reference_name in existing_references:
                continue

            references.append(
                LegalReference(
                    article=reference_name,
                    text=result.text,
                )
            )

            existing_references.add(
                reference_name
            )

            if len(references) >= limit:
                break

        return references