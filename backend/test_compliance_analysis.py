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
from app.services.requirement_retrieval_service import (
    RequirementRetrievalService,
)


db = SessionLocal()

try:
    requirement = next(
        requirement
        for requirement in REQUIREMENTS
        if requirement.requirement_id == "REQ-014"
    )

    retrieval_service = RequirementRetrievalService()

    legal_references = retrieval_service.retrieve_for_requirement(
        db=db,
        requirement=requirement,
        limit=3,
    )

    profile = SystemProfile(
        system_purpose="AI-assisted recruitment system",
        intended_users=["HR staff"],
        domain="Employment",
        personal_data=True,
        automated_decisions=["Candidate ranking"],
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

    analysis_service = ComplianceAnalysisService()

    assessment = analysis_service.assess_requirement(
        profile=profile,
        user_evidence=user_evidence,
        requirement=requirement,
        legal_references=legal_references,
    )

    print(assessment.model_dump_json(indent=2))

finally:
    db.close()