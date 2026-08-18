from unittest.mock import MagicMock

from app.db.database import SessionLocal
from app.models.compliance import (
    ComplianceAssessment,
    ComplianceStatus,
)
from app.models.evidence import ProfileEvidence
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)
from app.services.compliance_analysis_service import (
    ComplianceAnalysisService,
)
from app.services.requirement_registry import REQUIREMENTS


def test_only_relevant_requirement_uses_llm():

    db = SessionLocal()

    try:
        profile = SystemProfile(
            system_purpose="AI-assisted recruitment system",
            intended_users=["HR staff"],
            domain="Employment",
            personal_data=True,
            automated_decisions=[
                "Candidate ranking"
            ],
            human_oversight=HumanOversight(
                present=True,
                description=(
                    "HR staff review recommendations "
                    "before final decisions."
                ),
            ),
        )

        user_evidence = [
            ProfileEvidence(
                field="human_oversight",
                value="HR review before final decisions",
                source_type="page",
                source_number=4,
                quote=(
                    "HR staff review the generated "
                    "recommendations before making "
                    "the final hiring decision."
                ),
            )
        ]

        service = ComplianceAnalysisService()

        service.assess_requirement = MagicMock(
            return_value=ComplianceAssessment(
                requirement_id="REQ-014",
                status=ComplianceStatus.partial,
                explanation=(
                    "Human oversight exists, but additional "
                    "controls are not documented."
                ),
                user_evidence=[
                    "HR staff review recommendations."
                ],
                legal_references=[],
                recommendations=[
                    "Document override procedures."
                ],
            )
        )

        assessments = service.assess_all_requirements(
            db=db,
            profile=profile,
            user_evidence=user_evidence,
            requirements=REQUIREMENTS,
        )

        assert len(assessments) == 7

        assert (
            service.assess_requirement.call_count
            == 1
        )

        statuses = {
            assessment.requirement_id:
            assessment.status
            for assessment in assessments
        }

        assert (
            statuses["REQ-014"]
            == ComplianceStatus.partial
        )

        assert (
            statuses["REQ-009"]
            == ComplianceStatus.unknown
        )

        assert (
            statuses["REQ-015"]
            == ComplianceStatus.unknown
        )

    finally:
        db.close()