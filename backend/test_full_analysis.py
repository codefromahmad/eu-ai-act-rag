from app.db.database import SessionLocal
from app.models.evidence import ProfileEvidence
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)
from app.services.full_analysis_service import (
    FullAnalysisService,
)


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

    service = FullAnalysisService()

    result = service.analyze(
        db=db,
        profile=profile,
        user_evidence=user_evidence,
    )

    print(
        result.model_dump_json(
            indent=2
        )
    )

finally:
    db.close()