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


def test_pipeline_orchestrates_services():

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
                description=(
                    "HR reviews recommendations."
                ),
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

        service.document_extraction_service.extract = (
            MagicMock(
                return_value=extracted_document
            )
        )

        service.profile_service.extract_profile = (
            MagicMock(
                return_value=SystemProfileExtraction(
                    profile=profile,
                    evidence=evidence,
                )
            )
        )

        service.analysis_service.analyze = (
            MagicMock(
                return_value=analysis
            )
        )

        service.report_service.generate_report = (
            MagicMock(
                return_value=report
            )
        )

        # Avoid writing a real DB row in this unit test.
        from app.repositories.analysis_repository import (
            AnalysisRepository,
        )

        fake_saved = MagicMock()
        fake_saved.analysis_id = "test-analysis-id"

        original_save = AnalysisRepository.save

        AnalysisRepository.save = MagicMock(
            return_value=fake_saved
        )

        try:
            result = service.analyze_document(
                db=db,
                file_path="fake.txt",
                original_filename="system.txt",
            )

        finally:
            AnalysisRepository.save = original_save

        assert result["analysis_id"] == "test-analysis-id"
        assert result["filename"] == "system.txt"
        assert result["file_type"] == "txt"

        assert (
            service
            .document_extraction_service
            .extract
            .call_count
            == 1
        )

        assert (
            service
            .profile_service
            .extract_profile
            .call_count
            == 1
        )

        assert (
            service.analysis_service.analyze.call_count
            == 1
        )

        assert (
            service
            .report_service
            .generate_report
            .call_count
            == 1
        )

    finally:
        db.close()