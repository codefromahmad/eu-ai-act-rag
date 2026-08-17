from app.db.database import SessionLocal
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)
from app.services.risk_classification_service import (
    RiskClassificationService,
)


db = SessionLocal()

try:
    profile = SystemProfile(
        system_purpose=(
            "AI-assisted recruitment system"
        ),
        intended_users=[
            "HR staff"
        ],
        domain="Employment",
        deployment_context=(
            "Enterprise recruitment"
        ),
        personal_data=True,
        automated_decisions=[
            "Candidate ranking"
        ],
        human_oversight=HumanOversight(
            present=True,
            description=(
                "HR staff review recommendations "
                "before final hiring decisions."
            ),
        ),
    )

    service = RiskClassificationService()

    classification = service.classify(
        db=db,
        profile=profile,
    )

    print(
        classification.model_dump_json(
            indent=2
        )
    )

finally:
    db.close()