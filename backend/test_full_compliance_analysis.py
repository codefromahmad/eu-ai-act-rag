from app.db.database import SessionLocal
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
        risk_controls=[
            "Manual review before hiring decision"
        ],
        monitoring=None,
        security=None,
        transparency=None,
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

    assessments = service.assess_all_requirements(
        db=db,
        profile=profile,
        user_evidence=user_evidence,
        requirements=REQUIREMENTS,
    )

    print(
        "Total assessments:",
        len(assessments),
    )

    for assessment in assessments:

        print("\n" + "=" * 70)

        print(
            assessment.requirement_id,
            assessment.status.value,
        )

        print(
            assessment.explanation[:500]
        )

finally:
    db.close()