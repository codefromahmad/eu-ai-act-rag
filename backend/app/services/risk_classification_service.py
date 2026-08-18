import json

from sqlalchemy.orm import Session

from app.db.models.legal_chunk import LegalChunkDB
from app.models.risk_classification import RiskClassification
from app.models.system_profile import SystemProfile
from app.services.classification_retrieval_service import (
    ClassificationRetrievalService,
)
from app.services.llm_service import LLMService


class RiskClassificationService:

    def __init__(self):
        self.llm = LLMService()

        self.classification_retrieval = (
            ClassificationRetrievalService()
        )

    def _get_article_5(
        self,
        db: Session,
    ) -> dict | None:

        article_5 = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.article == "Article 5"
            )
            .first()
        )

        if not article_5:
            return None

        return {
            "type": "article",
            "reference": article_5.article,
            "text": article_5.text,
        }

    def classify(
        self,
        db: Session,
        profile: SystemProfile,
    ) -> RiskClassification:

        # --------------------------------------------------
        # 1. Retrieve only the two core classification sources
        # --------------------------------------------------

        classification_references = (
            self.classification_retrieval.retrieve(
                db=db,
                query=(
                    f"{profile.system_purpose} "
                    f"{profile.domain or ''} "
                    f"{' '.join(profile.automated_decisions or [])}"
                ),
                limit=2,
            )
        )

        legal_evidence = [
            {
                "type": (
                    "annex"
                    if reference.article.startswith("Annex")
                    else "article"
                ),
                "reference": reference.article,
                "text": reference.text,
            }
            for reference in classification_references
        ]

        # --------------------------------------------------
        # 2. Add Article 5 for prohibited-practice checks
        # --------------------------------------------------

        article_5 = self._get_article_5(
            db=db
        )

        if article_5:
            legal_evidence.insert(
                0,
                article_5,
            )

        # --------------------------------------------------
        # 3. Ask LLM using only:
        #    Article 5 + Article 6 + Annex III
        # --------------------------------------------------

        system_prompt = """
You are performing a preliminary EU AI Act applicability
and risk classification.

Base your classification only on:

1. The supplied AI system profile.
2. The supplied EU AI Act legal evidence.

Important rules:

- Do not rely on remembered article numbers.
- Do not invent legal requirements.
- Only cite articles or annexes contained in the supplied evidence.
- If the evidence is insufficient, classify the system as "uncertain".
- Do not claim definitive legal classification.
- Treat missing information as uncertainty.
- Use Article 5 for prohibited AI practices.
- Use Article 6 and Annex III for high-risk classification.

Available categories:

- prohibited
- high_risk
- limited_risk
- minimal_risk
- uncertain

Return only valid JSON.
"""

        payload = {
            "system_profile": profile.model_dump(),
            "legal_evidence": legal_evidence,
        }

        schema = (
            RiskClassification.model_json_schema()
        )

        user_prompt = f"""
Perform a preliminary EU AI Act risk classification.

INPUT:

{json.dumps(payload, indent=2)}

Return JSON matching this schema:

{json.dumps(schema, indent=2)}
"""

        raw_response = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        data = json.loads(
            raw_response
        )

        return RiskClassification.model_validate(
            data
        )