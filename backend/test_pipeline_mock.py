from unittest.mock import MagicMock

from app.db.database import SessionLocal
from app.models.analysis_result import (
    AnalysisScore,
    FullComplianceAnalysis,
)
from app.models.evidence import (
    ProfileEvidence,
    SystemProfileExtraction,
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
from app.services.compliance_pipeline_service import (
    CompliancePipelineService,
)


db = SessionLocal()

try:
    service = CompliancePipelineService()

    profile = SystemProfile(
        system_purpose="AI-assisted recruitment",
        intended_users=["HR staff"],
        domain="Employment",
        personal_data=True,
        automated_decisions=[
            "Candidate ranking"
        ],
        human_oversight=HumanOversight(
            present=True,
            description="HR reviews recommendations.",
        ),
    )

    evidence = [
        ProfileEvidence(
            field="human_oversight",
            value="Human review",
            page_number=4,
            quote="HR reviews recommendations.",
        )
    ]

    risk = RiskClassification(
        category=RiskCategory.high_risk,
        ai_act_applicable=True,
        explanation="Recruitment use.",
        relevant_articles=["Article 6"],
        relevant_annexes=["Annex III"],
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

    analysis = FullComplianceAnalysis(
        risk_classification=risk,
        assessments=[],
        score=score,
    )

    report = ComplianceReport(
        risk_classification=risk,
        score=score,
        summary=ReportSummary(
            executive_summary="Mock report.",
            strengths=[
                "Human oversight exists."
            ],
            weaknesses=[],
            missing_information=[
                "Additional controls are undocumented."
            ],
            recommendations=[
                "Provide more documentation."
            ],
        ),
        assessments=[],
    )

    # ----------------------------------------------
    # Mock external/expensive services
    # ----------------------------------------------

    service.profile_service.extract_profile = MagicMock(
        return_value=SystemProfileExtraction(
            profile=profile,
            evidence=evidence,
        )
    )

    service.analysis_service.analyze = MagicMock(
        return_value=analysis
    )

    service.report_service.generate_report = MagicMock(
        return_value=report
    )

    # Mock PDF extraction too
    from app.services.pdf_service import PDFService

    original_extract = PDFService.extract_text

    PDFService.extract_text = MagicMock(
        return_value={
            "filename": "test.pdf",
            "page_count": 5,
            "text": "AI recruitment system",
            "pages": [
                {
                    "page_number": 1,
                    "text": "AI recruitment system",
                }
            ],
        }
    )

    result = service.analyze_pdf(
        db=db,
        file_path="fake.pdf",
    )

    print(
        "Page count:",
        result["page_count"],
    )

    print(
        "System purpose:",
        result["system_profile"].system_purpose,
    )

    print(
        "Risk:",
        result["report"].risk_classification.category.value,
    )

    print(
        "Score:",
        result["report"].score.compliance_score,
    )

    print(
        "Profile extraction calls:",
        service.profile_service.extract_profile.call_count,
    )

    print(
        "Analysis calls:",
        service.analysis_service.analyze.call_count,
    )

    print(
        "Report calls:",
        service.report_service.generate_report.call_count,
    )

    PDFService.extract_text = original_extract

finally:
    db.close()