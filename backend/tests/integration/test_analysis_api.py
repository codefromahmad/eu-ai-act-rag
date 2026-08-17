from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.main import app
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


client = TestClient(app)


def create_test_analysis():

    db = SessionLocal()

    try:
        profile = SystemProfile(
            system_purpose="AI recruitment system",
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

        assessment = ComplianceAssessment(
            requirement_id="REQ-014",
            status=ComplianceStatus.partial,
            explanation="Human oversight is partially documented.",
            user_evidence=[
                "HR staff review recommendations."
            ],
            legal_references=[],
            recommendations=[
                "Document override procedures."
            ],
        )

        report = ComplianceReport(
            risk_classification=risk,
            score=score,
            summary=ReportSummary(
                executive_summary="Test report.",
                strengths=[
                    "Human oversight exists."
                ],
                weaknesses=[
                    "Oversight controls are incomplete."
                ],
                missing_information=[],
                recommendations=[
                    "Document more controls."
                ],
            ),
            assessments=[
                assessment
            ],
        )

        saved = AnalysisRepository.save(
            db=db,
            filename="integration_test.docx",
            file_type="docx",
            profile=profile,
            report=report,
        )

        return saved.analysis_id

    finally:
        db.close()


def test_get_analysis_by_id():

    analysis_id = create_test_analysis()

    response = client.get(
        f"/api/analyses/{analysis_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["analysis_id"] == analysis_id
    assert data["filename"] == "integration_test.docx"
    assert data["risk_category"] == "high_risk"
    assert data["compliance_score"] == 50.0


def test_get_all_analyses():

    response = client.get(
        "/api/analyses"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list,
    )


def test_analysis_not_found():

    response = client.get(
        "/api/analyses/non-existent-analysis-id"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Analysis not found."
    }