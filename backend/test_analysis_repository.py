from app.db.database import SessionLocal
from app.models.analysis_result import AnalysisScore
from app.models.compliance import (
    ComplianceAssessment,
    ComplianceStatus,
)
from app.models.report import (
    ComplianceReport,
    ReportSummary,
)
from app.models.risk_classification import (
    RiskCategory,
    RiskClassification,
)
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)
from app.repositories.analysis_repository import (
    AnalysisRepository,
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

    risk = RiskClassification(
        category=RiskCategory.high_risk,
        ai_act_applicable=True,
        explanation=(
            "Recruitment and candidate ranking "
            "appear to fall under the high-risk category."
        ),
        relevant_articles=[
            "Article 6"
        ],
        relevant_annexes=[
            "Annex III"
        ],
        indicators=[
            "Employment context",
            "Candidate ranking",
        ],
        missing_information=[],
        confidence=0.9,
    )

    score = AnalysisScore(
        compliance_score=50.0,
        coverage=14.29,
        total_requirements=7,
        known_requirements=1,
        compliant=0,
        partial=1,
        non_compliant=0,
        unknown=6,
    )

    assessments = [
        ComplianceAssessment(
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
    ]

    report = ComplianceReport(
        risk_classification=risk,
        score=score,
        summary=ReportSummary(
            executive_summary=(
                "The system appears high-risk and "
                "human oversight is only partially documented."
            ),
            strengths=[
                "Human oversight exists."
            ],
            weaknesses=[
                "Oversight controls are incomplete."
            ],
            missing_information=[
                "Risk management documentation.",
                "Data governance documentation.",
            ],
            recommendations=[
                "Document additional safeguards."
            ],
        ),
        assessments=assessments,
    )

    saved = AnalysisRepository.save(
        db=db,
        filename="test_system.docx",
        file_type="docx",
        profile=profile,
        report=report,
    )

    print(
        "Saved analysis ID:",
        saved.analysis_id,
    )

    print(
        "Filename:",
        saved.filename,
    )

    print(
        "Risk:",
        saved.risk_category,
    )

    print(
        "Score:",
        saved.compliance_score,
    )

    print(
        "Coverage:",
        saved.coverage,
    )

    fetched = (
        AnalysisRepository.get_by_analysis_id(
            db=db,
            analysis_id=saved.analysis_id,
        )
    )

    print(
        "Fetched successfully:",
        fetched is not None,
    )

    if fetched:
        print(
            "Fetched filename:",
            fetched.filename,
        )

finally:
    db.close()