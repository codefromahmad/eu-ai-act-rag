import json

from sqlalchemy.orm import Session

from app.models.compliance import (
    ComplianceAssessment,
    ComplianceRequirement,
    ComplianceStatus,
    LegalReference,
)
from app.models.evidence import ProfileEvidence
from app.models.system_profile import SystemProfile
from app.services.evidence_selection_service import (
    EvidenceSelectionService,
)
from app.services.llm_service import LLMService
from app.services.requirement_retrieval_service import (
    RequirementRetrievalService,
)


class ComplianceAnalysisService:

    def __init__(self):
        self.llm = LLMService()

        self.requirement_retrieval = (
            RequirementRetrievalService()
        )

        self.evidence_selection = (
            EvidenceSelectionService()
        )

    def _create_unknown_assessment(
        self,
        requirement: ComplianceRequirement,
        legal_references: list[LegalReference],
    ) -> ComplianceAssessment:
        """
        Create an UNKNOWN result without calling the LLM
        when the user's document contains no relevant evidence.
        """

        return ComplianceAssessment(
            requirement_id=requirement.requirement_id,

            status=ComplianceStatus.unknown,

            explanation=(
                "The uploaded documentation does not contain "
                "sufficient evidence related to this requirement. "
                "Therefore, compliance cannot be determined."
            ),

            user_evidence=[],

            legal_references=legal_references,

            recommendations=[
                (
                    "Provide documentation or evidence addressing: "
                    f"{requirement.description}"
                )
            ],
        )

    def assess_requirement(
        self,
        profile: SystemProfile,
        user_evidence: list[ProfileEvidence],
        requirement: ComplianceRequirement,
        legal_references: list[LegalReference],
    ) -> ComplianceAssessment:

        system_prompt = """
You are performing a preliminary EU AI Act compliance assessment.

Important rules:

1. Base your analysis only on:
   - the structured AI system profile,
   - evidence from the user's PDF,
   - the supplied EU AI Act legal references.

2. Do not invent facts.

3. Do not claim definitive legal compliance.

4. Use one of these statuses only:
   - compliant
   - partial
   - non_compliant
   - unknown

5. If the user's evidence is insufficient,
   use "unknown".

6. Keep legal evidence separate from user evidence.

7. Return only valid JSON.
"""

        payload = {
            "requirement": requirement.model_dump(),

            "system_profile": profile.model_dump(),

            "user_evidence": [
                evidence.model_dump()
                for evidence in user_evidence
            ],

            "legal_references": [
                reference.model_dump()
                for reference in legal_references
            ],
        }

        schema = (
            ComplianceAssessment.model_json_schema()
        )

        user_prompt = f"""
Assess the AI system against this single
EU AI Act compliance requirement.

INPUT:

{json.dumps(payload, indent=2)}

Your response must match this JSON schema:

{json.dumps(schema, indent=2)}
"""

        raw_response = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        data = json.loads(
            raw_response
        )

        assessment = (
            ComplianceAssessment.model_validate(
                data
            )
        )

        # Always use original database legal text.
        assessment.legal_references = (
            legal_references
        )

        return assessment

    def assess_all_requirements(
        self,
        db: Session,
        profile: SystemProfile,
        user_evidence: list[ProfileEvidence],
        requirements: list[ComplianceRequirement],
    ) -> list[ComplianceAssessment]:

        assessments: list[
            ComplianceAssessment
        ] = []

        for requirement in requirements:

            print(
                f"Analyzing "
                f"{requirement.requirement_id} "
                f"- {requirement.title}..."
            )

            # ------------------------------------------
            # 1. Retrieve legal evidence
            # ------------------------------------------

            legal_references = (
                self.requirement_retrieval
                .retrieve_for_requirement(
                    db=db,
                    requirement=requirement,
                    limit=3,
                )
            )

            # ------------------------------------------
            # 2. Select only relevant user evidence
            # ------------------------------------------

            relevant_evidence = (
                self.evidence_selection
                .select_for_requirement(
                    requirement_id=(
                        requirement.requirement_id
                    ),
                    evidence=user_evidence,
                )
            )

            # ------------------------------------------
            # 3. No evidence?
            #    Do NOT waste an LLM call.
            # ------------------------------------------

            if not relevant_evidence:

                assessment = (
                    self._create_unknown_assessment(
                        requirement=requirement,
                        legal_references=legal_references,
                    )
                )

                assessments.append(
                    assessment
                )

                print(
                    f"Completed "
                    f"{requirement.requirement_id}: "
                    "unknown "
                    "(no LLM call)"
                )

                continue

            # ------------------------------------------
            # 4. Evidence exists → use LLM reasoning
            # ------------------------------------------

            assessment = (
                self.assess_requirement(
                    profile=profile,
                    user_evidence=relevant_evidence,
                    requirement=requirement,
                    legal_references=legal_references,
                )
            )

            assessments.append(
                assessment
            )

            print(
                f"Completed "
                f"{requirement.requirement_id}: "
                f"{assessment.status.value}"
            )

        return assessments