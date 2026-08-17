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
from app.models.extracted_document import (
    DocumentSection,
    ExtractedDocument,
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
            page_number=1,
            quote="HR reviews recommendations.",
        )
    ]

    risk = RiskClassification(
        category=RiskCategory.high_risk,
        ai_act_applicable=True,
        explanation="Recruitment use.",
        relevant_articles=[
            "Article 6"
        ],
        relevant_annexes=[
            "Annex III"
        ],
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

    extracted_document = ExtractedDocument(
        filename="test_system.txt",
        file_type="txt",
        text="AI recruitment system",
        sections=[
            DocumentSection(
                section_number=1,
                text="AI recruitment system",
            )
        ],
        page_count=None,
    )

    # ----------------------------------------------
    # Mock document extraction
    # ----------------------------------------------

    service.document_extraction_service.extract = (
        MagicMock(
            return_value=extracted_document
        )
    )

    # ----------------------------------------------
    # Mock profile extraction
    # ----------------------------------------------

    service.profile_service.extract_profile = (
        MagicMock(
            return_value=SystemProfileExtraction(
                profile=profile,
                evidence=evidence,
            )
        )
    )

    # ----------------------------------------------
    # Mock compliance analysis
    # ----------------------------------------------

    service.analysis_service.analyze = (
        MagicMock(
            return_value=analysis
        )
    )

    # ----------------------------------------------
    # Mock report generation
    # ----------------------------------------------

    service.report_service.generate_report = (
        MagicMock(
            return_value=report
        )
    )

    result = service.analyze_document(
        db=db,
        file_path="fake.txt",
    )

    print(
        "Filename:",
        result["filename"],
    )

    print(
        "File type:",
        result["file_type"],
    )

    print(
        "Section count:",
        result["section_count"],
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
        "Document extraction calls:",
        (
            service
            .document_extraction_service
            .extract
            .call_count
        ),
    )

    print(
        "Profile extraction calls:",
        (
            service
            .profile_service
            .extract_profile
            .call_count
        ),
    )

    print(
        "Analysis calls:",
        service.analysis_service.analyze.call_count,
    )

    print(
        "Report calls:",
        (
            service
            .report_service
            .generate_report
            .call_count
        ),
    )

finally:
    db.close()