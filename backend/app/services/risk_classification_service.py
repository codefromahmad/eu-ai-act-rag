import json

from sqlalchemy.orm import Session

from app.db.models.legal_chunk import LegalChunkDB
from app.models.risk_classification import RiskClassification
from app.models.system_profile import SystemProfile
from app.services.llm_service import LLMService


class RiskClassificationService:

    def __init__(self):
        self.llm = LLMService()

    def _get_legal_evidence(
        self,
        db: Session,
    ) -> list[dict]:

        legal_chunks = []

        # Article 5 — prohibited AI practices
        article_5 = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.article == "Article 5"
            )
            .first()
        )

        if article_5:
            legal_chunks.append(
                {
                    "type": "article",
                    "reference": article_5.article,
                    "text": article_5.text,
                }
            )

        # Article 6 — high-risk classification rules
        article_6 = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.article == "Article 6"
            )
            .first()
        )

        if article_6:
            legal_chunks.append(
                {
                    "type": "article",
                    "reference": article_6.article,
                    "text": article_6.text,
                }
            )

        # Annex III — listed high-risk use cases
        annex_iii = (
            db.query(LegalChunkDB)
            .filter(
                LegalChunkDB.annex == "Annex III"
            )
            .first()
        )

        if annex_iii:
            legal_chunks.append(
                {
                    "type": "annex",
                    "reference": annex_iii.annex,
                    "text": annex_iii.text,
                }
            )

        return legal_chunks

    def classify(
        self,
        db: Session,
        profile: SystemProfile,
    ) -> RiskClassification:

        legal_evidence = self._get_legal_evidence(
            db=db
        )

        system_prompt = """
You are performing a preliminary EU AI Act applicability
and risk classification.

You must base your classification only on:

1. The supplied AI system profile.
2. The supplied EU AI Act legal evidence.

Important rules:

- Do not rely on remembered EU AI Act article numbers.
- Do not invent legal requirements.
- Only cite articles or annexes contained in the supplied legal evidence.
- If the evidence is insufficient, classify the system as "uncertain".
- Do not claim definitive legal classification.
- Treat missing information as uncertainty, not automatic non-compliance.

Available categories:

- prohibited
- high_risk
- limited_risk
- minimal_risk
- uncertain

Use Article 5 when evaluating potentially prohibited practices.

Use Article 6 and Annex III when evaluating whether a system
appears to qualify as high-risk.

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
Perform a preliminary EU AI Act risk classification
for the following AI system.

INPUT:

{json.dumps(payload, indent=2)}

Your response must match this JSON schema:

{json.dumps(schema, indent=2)}
"""

        raw_response = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        data = json.loads(raw_response)

        classification = (
            RiskClassification.model_validate(data)
        )

        return classification