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
            page_number=4,
            quote=(
                "HR staff review the generated recommendations "
                "before making the final hiring decision."
            ),
        )
    ]

    service = ComplianceAnalysisService()

    # --------------------------------------------------
    # Replace the real LLM call with a mock
    # --------------------------------------------------

    service.assess_requirement = MagicMock(
        return_value=ComplianceAssessment(
            requirement_id="REQ-014",
            status=ComplianceStatus.partial,
            explanation=(
                "Human oversight exists, but additional "
                "controls are not documented."
            ),
            user_evidence=[
                (
                    "HR staff review recommendations "
                    "before final decisions."
                )
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

    print("\nTotal assessments:", len(assessments))

    print(
        "LLM-backed assessments:",
        service.assess_requirement.call_count,
    )

    print("\n--- RESULTS ---")

    for assessment in assessments:
        print(
            assessment.requirement_id,
            "→",
            assessment.status.value,
        )

finally:
    db.close()